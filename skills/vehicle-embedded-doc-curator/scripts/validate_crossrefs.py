#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


VALID_STATUSES = {"candidate", "needs-review", "verified", "rejected"}


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


def validate_file(path: Path) -> list[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    if text.strip() in {"", "[]"}:
        return []
    issues = []
    entries = split_entries(text)
    if not entries:
        return [f"{path.name}: expected a YAML list"]
    for idx, entry in enumerate(entries):
        prefix = f"{path.name}[{idx}]"
        entry_id = scalar(entry, "id")
        status = scalar(entry, "status")
        relation = scalar(entry, "relation")
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
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate simple cross reference YAML files without external dependencies.")
    parser.add_argument("memory_dir", help=".vehicle-embedded-docs directory")
    args = parser.parse_args()

    memory = Path(args.memory_dir).resolve()
    files = [
        memory / "crossrefs" / "candidate-links.yml",
        memory / "crossrefs" / "verified-links.yml",
        memory / "crossrefs" / "conflicts.yml",
    ]

    issues = []
    for path in files:
        issues.extend(validate_file(path))

    if issues:
        for issue in issues:
            print(issue)
        return 1
    print("crossrefs ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
