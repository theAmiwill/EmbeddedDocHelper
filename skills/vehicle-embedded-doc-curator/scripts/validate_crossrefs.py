#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


VALID_STATUSES = {"candidate", "needs-review", "verified", "rejected"}
PROJECT_ONLY_PATTERNS = [
    r"\bproject/",
    r"\bcode/",
    r"\bcode_context_only\b",
    r"\.arxml\b",
    r"\.c\b",
    r"\.h\b",
    r"\bcurrent project\b",
    r"\blocal configuration\b",
]


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


def has_evidence(entry: str) -> bool:
    return re.search(r"(?m)^\s*evidence:\s*$", entry) is not None or re.search(r"(?m)^\s*evidence:\s*\[.+\]\s*$", entry) is not None


def mentions_project_only(entry: str) -> bool:
    return any(re.search(pattern, entry, re.IGNORECASE) for pattern in PROJECT_ONLY_PATTERNS)


def validate_file(path: Path, scope: str) -> list[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    if text.strip() in {"", "[]"}:
        return []
    issues = []
    entries = split_entries(text)
    if not entries:
        return [f"{path}: expected a YAML list"]
    for idx, entry in enumerate(entries):
        prefix = f"{path.relative_to(path.anchor) if path.is_absolute() else path}[{idx}]"
        entry_id = scalar(entry, "id")
        status = scalar(entry, "status")
        relation = scalar(entry, "relation")
        portability = scalar(entry, "portability")
        if not entry_id:
            issues.append(f"{prefix}: missing id")
        if status not in VALID_STATUSES:
            issues.append(f"{prefix}: invalid status {status!r}")
        if not relation:
            issues.append(f"{prefix}: missing relation")
        if status in {"candidate", "needs-review", "verified"} and not has_evidence(entry):
            issues.append(f"{prefix}: missing evidence")
        if status == "verified" and scalar(entry, "verified_by_user") != "true":
            issues.append(f"{prefix}: verified entry must have verified_by_user: true")
        if scope == "portable":
            if portability and portability != "portable":
                issues.append(f"{prefix}: portable crossref has portability {portability!r}")
            if status == "verified" and mentions_project_only(entry):
                issues.append(f"{prefix}: portable verified entry mentions project/code-only material")
    return issues


def crossref_dirs(memory: Path) -> list[tuple[str, Path]]:
    dirs: list[tuple[str, Path]] = []
    legacy = memory / "crossrefs"
    if legacy.exists():
        dirs.append(("project", legacy))
    portable = memory / "portable" / "crossrefs"
    if portable.exists():
        dirs.append(("portable", portable))
    project = memory / "project" / "crossrefs"
    if project.exists():
        dirs.append(("project", project))
    return dirs


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate simple cross reference YAML files without external dependencies.")
    parser.add_argument("memory_dir", help=".vehicle-embedded-docs directory")
    parser.add_argument("--scope", choices=["auto", "portable", "project"], default="auto", help="Validate one scope or auto-detect all scopes")
    args = parser.parse_args()

    memory = Path(args.memory_dir).resolve()
    if args.scope == "auto":
        dirs = crossref_dirs(memory)
    else:
        dirs = [(args.scope, memory / args.scope / "crossrefs")]
        if args.scope == "portable":
            dirs = [("portable", memory / "portable" / "crossrefs")]
        if args.scope == "project":
            dirs = [("project", memory / "project" / "crossrefs")]

    issues = []
    for scope, directory in dirs:
        for name in ("candidate-links.yml", "verified-links.yml", "conflicts.yml"):
            issues.extend(validate_file(directory / name, scope))

    if issues:
        for issue in issues:
            print(issue)
        return 1
    print("crossrefs ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
