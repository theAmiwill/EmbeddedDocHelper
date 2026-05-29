#!/usr/bin/env python3
import argparse
import re
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path


INDEX_EXTENSIONS = {".yml", ".yaml", ".md", ".txt"}
SKIP_PARTS = {"crossrefs", "audit", "features", "lessons"}
GENERIC_LOW_CONFIDENCE = {"CLOCK", "RESET", "INTERRUPT", "PIN", "PINMUX", "POWER", "SOFTWARE-STACK"}
TERM_PATTERNS = [
    r"\bWDG_17_AVWDT\b",
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
    r"\bBFX\b",
    r"\bBMC\b",
    r"\bCRC\b",
    r"\bTINFRA\b",
    r"\bRVLIB\b",
    r"\bCLOCK\b",
    r"\bRESET\b",
    r"\bINTERRUPT\b",
    r"\bPINMUX\b",
    r"\bPIN\b",
    r"\bPOWER\b",
]

SOFTWARE_SUBTYPE_ORDER = {
    "autosar_standard": 10,
    "vendor_requirement": 20,
    "vendor_mcal_manual": 30,
    "tool_guide": 40,
    "build_install_guide": 50,
    "demo_app_guide": 60,
    "software_general": 70,
}

SOFTWARE_PAIR_LABELS = {
    frozenset({"autosar_standard", "vendor_requirement"}): "AUTOSAR requirement material and vendor requirement extract",
    frozenset({"vendor_requirement", "vendor_mcal_manual"}): "vendor requirement extract and MCAL user manual",
    frozenset({"vendor_mcal_manual", "tool_guide"}): "MCAL user manual and tool guide",
    frozenset({"vendor_mcal_manual", "build_install_guide"}): "MCAL user manual and build/install guide",
    frozenset({"vendor_mcal_manual", "demo_app_guide"}): "MCAL user manual and demo application guide",
    frozenset({"tool_guide", "build_install_guide"}): "tool guide and build/install guide",
    frozenset({"tool_guide", "demo_app_guide"}): "tool guide and demo application guide",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")


def read_limited(path: Path, limit: int = 200_000) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    return text[:limit]


def normalize_term(term: str) -> str:
    term = term.upper()
    if term == "ETHERNET":
        return "ETH"
    return term


def terms_for(path: Path, text: str) -> set[str]:
    haystack = f"{path.as_posix()}\n{text}".upper()
    terms: set[str] = set()
    for pattern in TERM_PATTERNS:
        for match in re.finditer(pattern, haystack):
            terms.add(normalize_term(match.group(0)))
    return terms


def software_subtype(rel_path: str, text: str) -> str | None:
    haystack = f"{rel_path}\n{text}".upper()
    if "BUILD_INSTALLATION" in haystack or "BUILD-INSTALLATION" in haystack or "BUILD INSTALLATION" in haystack or "INSTALLATION" in haystack:
        return "build_install_guide"
    if "DEMOAPP" in haystack or "DEMO_APP" in haystack or "DEMO APP" in haystack or "DEMO APPLICATION" in haystack:
        return "demo_app_guide"
    if "AUTOSAR" in haystack or re.search(r"R\d{2}[-_ ]?\d{2}", haystack):
        return "autosar_standard"
    if "REQ_EXTRACT" in haystack or "REQ-EXTRACT" in haystack or "REQ EXTRACT" in haystack:
        return "vendor_requirement"
    if "MCAL" in haystack or "DRIVERS_UM" in haystack or "_UM_" in haystack or "_UM." in haystack or "USER MANUAL" in haystack or "MODULE USER MANUAL" in haystack:
        return "vendor_mcal_manual"
    if re.search(r"\b(EB|STUDIO|DAVINCI|TRESOS|CONFIGURATOR)\b", haystack) or "CONFIGURATION TOOL" in haystack:
        return "tool_guide"
    if re.search(r"\b(BSW|RTE|AUTOSAR|MCAL|CONFIGURATION|GENERATED FILES?)\b", haystack):
        return "software_general"
    return None


def classify(rel_path: str, text: str) -> tuple[str, str, str | None] | None:
    if rel_path.startswith("portable/hardware/"):
        return ("portable", "hardware", None)
    if rel_path.startswith("portable/software/"):
        return ("portable", "software", software_subtype(rel_path, text) or "software_general")
    if rel_path.startswith("project/code/"):
        return ("project", "code", None)
    if rel_path.startswith("project/schematics/") or rel_path.startswith("schematics/"):
        return ("project", "hardware", None)
    if rel_path.startswith("manuals/"):
        subtype = software_subtype(rel_path, text)
        if subtype:
            return ("portable", "software", subtype)
    return None


def iter_artifacts(memory: Path) -> list[dict]:
    artifacts = []
    for path in sorted(memory.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in INDEX_EXTENSIONS:
            continue
        rel_path = rel(path, memory)
        if any(part in SKIP_PARTS for part in Path(rel_path).parts):
            continue
        text = read_limited(path)
        classified = classify(rel_path, text)
        if classified is None:
            continue
        terms = terms_for(path, text)
        scope, source_class, subtype = classified
        if not terms and source_class != "software":
            continue
        artifacts.append(
            {
                "path": rel_path,
                "scope": scope,
                "class": source_class,
                "subtype": subtype,
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


def source_slug(path: str) -> str:
    stem = Path(path).stem
    return slug(stem)[-40:]


def confidence(term: str, subtype_pair: bool = False) -> str:
    if term in GENERIC_LOW_CONFIDENCE:
        return "low"
    if subtype_pair:
        return "medium"
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


def software_pair_label(left: dict, right: dict) -> str | None:
    return SOFTWARE_PAIR_LABELS.get(frozenset({left["subtype"], right["subtype"]}))


def software_pair_terms(left: dict, right: dict) -> list[str]:
    common = sorted(left["terms"] & right["terms"])
    if common:
        return common
    left_specific = left["terms"] - GENERIC_LOW_CONFIDENCE
    right_specific = right["terms"] - GENERIC_LOW_CONFIDENCE
    if software_pair_label(left, right) and not (left_specific and right_specific):
        return ["SOFTWARE-STACK"]
    return []


def software_entry(term: str, left: dict, right: dict) -> str:
    left_subtype = left["subtype"] or "software_general"
    right_subtype = right["subtype"] or "software_general"
    ordered = sorted([left, right], key=lambda item: SOFTWARE_SUBTYPE_ORDER.get(item["subtype"] or "software_general", 99))
    left, right = ordered[0], ordered[1]
    label = software_pair_label(left, right) or f"{left_subtype} and {right_subtype}"
    term_slug = "stack" if term == "SOFTWARE-STACK" else slug(term)
    entry_id = f"bootstrap-portable-{term_slug}-software-{slug(left['subtype'] or 'software')}-{slug(right['subtype'] or 'software')}-{source_slug(left['path'])}-{source_slug(right['path'])}"
    relation_term = "the software stack" if term == "SOFTWARE-STACK" else term
    return "\n".join(
        [
            f"- id: {entry_id}",
            "  status: candidate",
            "  portability: portable",
            f'  relation: "{relation_term} appears across {label}; verify how these software documents constrain or explain each other."',
            f"  confidence: {confidence(term, subtype_pair=True)}",
            "  evidence:",
            evidence(left["path"], term),
            evidence(right["path"], term),
            f"  software_subtypes: [{left['subtype']}, {right['subtype']}]",
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


def software_entries(artifacts: list[dict], existing: set[str], max_entries: int) -> list[str]:
    software = [item for item in artifacts if item["scope"] == "portable" and item["class"] == "software"]
    entries: list[str] = []
    seen: set[str] = set()
    for left, right in combinations(software, 2):
        if left["path"] == right["path"]:
            continue
        if not software_pair_label(left, right) and not (left["terms"] & right["terms"]):
            continue
        for term in software_pair_terms(left, right):
            entry = software_entry(term, left, right)
            entry_id = scalar(entry, "id")
            if entry_id not in existing and entry_id not in seen:
                entries.append(entry)
                seen.add(entry_id)
            if len(entries) >= max_entries:
                return entries
    return entries


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
        memory / "crossrefs" / "candidate-links.yml",
        memory / "crossrefs" / "verified-links.yml",
    )

    for term in sorted(set(portable_hardware) & set(portable_software)):
        entry = portable_entry(term, portable_hardware[term], portable_software[term])
        if scalar(entry, "id") not in existing:
            portable_entries.append(entry)
        if len(portable_entries) >= max_entries:
            break

    remaining_portable = max(max_entries - len(portable_entries), 0)
    portable_entries.extend(software_entries(artifacts, existing, remaining_portable))

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
                "software_software_candidates_enabled: true",
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
