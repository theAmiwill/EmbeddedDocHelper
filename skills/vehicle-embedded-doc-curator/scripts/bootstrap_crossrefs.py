#!/usr/bin/env python3
import argparse
import re
from datetime import datetime, timezone
from pathlib import Path


INDEX_EXTENSIONS = {".yml", ".yaml", ".md", ".txt"}
SKIP_PARTS = {"crossrefs", "audit", "features", "lessons"}
GENERIC_LOW_CONFIDENCE = {"CLOCK", "RESET", "INTERRUPT", "PIN", "PINMUX", "POWER"}
TERM_PATTERNS = [
    r"\bCAN\d*\b",
    r"\bLIN\d*\b",
    r"\bSPI\d*\b",
    r"\bADC\d*\b",
    r"\bPWM\d*\b",
    r"\bDIO\b",
    r"\bPORT\b",
    r"\bMCU\b",
    r"\bGPT\b",
    r"\bWDG\b",
    r"\bETH(?:ERNET)?\b",
    r"\bICU\b",
    r"\bOCU\b",
    r"\bDMA\b",
    r"\bCLOCK\b",
    r"\bRESET\b",
    r"\bINTERRUPT\b",
    r"\bPINMUX\b",
    r"\bPIN\b",
    r"\bPOWER\b",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")


def read_limited(path: Path, limit: int = 200_000) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    return text[:limit]


def terms_for(path: Path, text: str) -> set[str]:
    haystack = f"{path.as_posix()}\n{text}".upper()
    terms: set[str] = set()
    for pattern in TERM_PATTERNS:
        for match in re.finditer(pattern, haystack):
            term = match.group(0)
            if term == "ETHERNET":
                term = "ETH"
            terms.add(term)
    return terms


def classify(rel_path: str) -> tuple[str, str] | None:
    if rel_path.startswith("portable/hardware/"):
        return ("portable", "hardware")
    if rel_path.startswith("portable/software/"):
        return ("portable", "software")
    if rel_path.startswith("project/code/"):
        return ("project", "code")
    if rel_path.startswith("project/schematics/"):
        return ("project", "hardware")
    if rel_path.startswith("schematics/"):
        return ("project", "hardware")
    return None


def iter_artifacts(memory: Path) -> list[dict]:
    artifacts = []
    for path in sorted(memory.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in INDEX_EXTENSIONS:
            continue
        rel_path = rel(path, memory)
        if any(part in SKIP_PARTS for part in Path(rel_path).parts):
            continue
        classified = classify(rel_path)
        if classified is None:
            continue
        text = read_limited(path)
        terms = terms_for(path, text)
        if not terms:
            continue
        scope, source_class = classified
        artifacts.append(
            {
                "path": rel_path,
                "scope": scope,
                "class": source_class,
                "terms": terms,
            }
        )
    return artifacts


def split_entries(text: str) -> list[str]:
    entries: list[list[str]] = []
    current: list[str] = []
    for line in text.splitlines():
        if line.startswith("- ") and current:
            entries.append(current)
            current = [line]
        elif line.startswith("- "):
            current = [line]
        elif current:
            current.append(line)
    if current:
        entries.append(current)
    return ["\n".join(entry) for entry in entries]


def scalar(entry: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*(?:-\s*)?{re.escape(key)}:\s*(.+?)\s*$", entry)
    if not match:
        return None
    return match.group(1).strip().strip('"').strip("'")


def existing_ids(*paths: Path) -> set[str]:
    ids: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        for entry in split_entries(path.read_text(encoding="utf-8", errors="replace")):
            entry_id = scalar(entry, "id")
            if entry_id:
                ids.add(entry_id)
    return ids


def append_entries(path: Path, entries: list[str]) -> None:
    if not entries:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8", errors="replace") if path.exists() else "[]\n"
    existing_entries = split_entries(existing)
    all_entries = existing_entries + entries
    path.write_text("\n".join(entry.rstrip() for entry in all_entries) + "\n", encoding="utf-8")


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def confidence(term: str) -> str:
    if term in GENERIC_LOW_CONFIDENCE:
        return "low"
    return "medium"


def evidence(path: str, term: str) -> str:
    return f'    - source: {path}\n      ref: "bootstrap term: {term}"'


def portable_entry(term: str, hardware: dict, software: dict) -> str:
    entry_id = f"bootstrap-portable-{slug(term)}-hardware-software"
    return "\n".join(
        [
            f"- id: {entry_id}",
            "  status: candidate",
            "  portability: portable",
            f'  relation: "{term} appears in portable hardware and software indexes; verify whether the hardware facts map to the software configuration guide."',
            f"  confidence: {confidence(term)}",
            "  evidence:",
            evidence(hardware["path"], term),
            evidence(software["path"], term),
            '  created_from_query: "Initial curator crossref bootstrap"',
            "  generated_by: bootstrap_crossrefs.py",
            "  verified_by_user: false",
        ]
    )


def project_entry(term: str, left: dict, right: dict) -> str:
    classes = "-".join(sorted({left["class"], right["class"]}))
    entry_id = f"bootstrap-project-{slug(term)}-{slug(classes)}"
    return "\n".join(
        [
            f"- id: {entry_id}",
            "  status: candidate",
            "  portability: project",
            '  authority_role: code_context_only' if "code" in {left["class"], right["class"]} else "  authority_role: hardware_primary",
            f'  relation: "{term} appears in project-specific indexes and related hardware/software material; verify the project-specific relationship before relying on it."',
            f"  confidence: {confidence(term)}",
            "  evidence:",
            evidence(left["path"], term),
            evidence(right["path"], term),
            '  created_from_query: "Initial curator crossref bootstrap"',
            "  generated_by: bootstrap_crossrefs.py",
            "  verified_by_user: false",
        ]
    )


def first_by_term(artifacts: list[dict], scope: str | None = None, source_class: str | None = None) -> dict[str, dict]:
    result: dict[str, dict] = {}
    for artifact in artifacts:
        if scope and artifact["scope"] != scope:
            continue
        if source_class and artifact["class"] != source_class:
            continue
        for term in sorted(artifact["terms"]):
            result.setdefault(term, artifact)
    return result


def build_entries(memory: Path, max_entries: int) -> tuple[list[str], list[str]]:
    artifacts = iter_artifacts(memory)
    portable_hardware = first_by_term(artifacts, "portable", "hardware")
    portable_software = first_by_term(artifacts, "portable", "software")
    project_hardware = first_by_term(artifacts, "project", "hardware")
    project_code = first_by_term(artifacts, "project", "code")

    portable_entries = []
    project_entries = []

    existing = existing_ids(
        memory / "portable" / "crossrefs" / "candidate-links.yml",
        memory / "portable" / "crossrefs" / "verified-links.yml",
        memory / "project" / "crossrefs" / "candidate-links.yml",
        memory / "project" / "crossrefs" / "verified-links.yml",
    )

    for term in sorted(set(portable_hardware) & set(portable_software)):
        entry = portable_entry(term, portable_hardware[term], portable_software[term])
        if scalar(entry, "id") not in existing:
            portable_entries.append(entry)
        if len(portable_entries) >= max_entries:
            break

    project_pairs: list[tuple[str, dict, dict]] = []
    for term in sorted(set(project_code) & set(portable_hardware)):
        project_pairs.append((term, project_code[term], portable_hardware[term]))
    for term in sorted(set(project_code) & set(portable_software)):
        project_pairs.append((term, project_code[term], portable_software[term]))
    for term in sorted(set(project_hardware) & set(portable_hardware)):
        project_pairs.append((term, project_hardware[term], portable_hardware[term]))
    for term in sorted(set(project_hardware) & set(portable_software)):
        project_pairs.append((term, project_hardware[term], portable_software[term]))
    for term in sorted(set(project_hardware) & set(project_code)):
        project_pairs.append((term, project_hardware[term], project_code[term]))

    seen_project_ids: set[str] = set()
    for term, left, right in project_pairs:
        entry = project_entry(term, left, right)
        entry_id = scalar(entry, "id")
        if entry_id not in existing and entry_id not in seen_project_ids:
            project_entries.append(entry)
            seen_project_ids.add(entry_id)
        if len(project_entries) >= max_entries:
            break

    return portable_entries, project_entries


def write_audit(memory: Path, portable_count: int, project_count: int) -> None:
    audit = memory / "audit" / "crossref-bootstrap.yml"
    audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(
        "\n".join(
            [
                f'last_run_at: "{now_utc()}"',
                "generated_by: bootstrap_crossrefs.py",
                f"portable_candidates_added: {portable_count}",
                f"project_candidates_added: {project_count}",
                'policy: "candidate-only; generated from existing indexes; requires source recheck and explicit user approval before promotion"',
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate first-use candidate cross references from existing .vehicle-embedded-docs indexes.")
    parser.add_argument("memory_dir", help=".vehicle-embedded-docs directory")
    parser.add_argument("--force", action="store_true", help="Run even when audit/crossref-bootstrap.yml already exists")
    parser.add_argument("--max-entries", type=int, default=50, help="Maximum entries per scope")
    args = parser.parse_args()

    memory = Path(args.memory_dir).resolve()
    if not (memory / "manifest.yml").exists():
        raise SystemExit(f"not a .vehicle-embedded-docs memory directory: {memory}")

    audit = memory / "audit" / "crossref-bootstrap.yml"
    if audit.exists() and not args.force:
        print(f"bootstrap already recorded: {audit}")
        return 0

    portable_entries, project_entries = build_entries(memory, args.max_entries)
    append_entries(memory / "portable" / "crossrefs" / "candidate-links.yml", portable_entries)
    append_entries(memory / "project" / "crossrefs" / "candidate-links.yml", project_entries)
    write_audit(memory, len(portable_entries), len(project_entries))
    print(f"portable candidates added: {len(portable_entries)}")
    print(f"project candidates added: {len(project_entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
