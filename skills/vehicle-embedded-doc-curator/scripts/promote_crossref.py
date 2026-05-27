#!/usr/bin/env python3
import argparse
import re
from datetime import datetime, timezone
from pathlib import Path


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


def replace_or_add(entry: str, key: str, value: str) -> str:
    pattern = rf"(?m)^(\s*){re.escape(key)}:\s*.*$"
    replacement = rf"\1{key}: {value}"
    if re.search(pattern, entry):
        return re.sub(pattern, replacement, entry)
    return entry.rstrip() + f"\n  {key}: {value}"


def has_evidence(entry: str) -> bool:
    return re.search(r"(?m)^\s*evidence:\s*$", entry) is not None or re.search(r"(?m)^\s*evidence:\s*\[.+\]\s*$", entry) is not None


def mentions_project_only(entry: str) -> bool:
    return any(re.search(pattern, entry, re.IGNORECASE) for pattern in PROJECT_ONLY_PATTERNS)


def write_entries(path: Path, entries: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not entries:
        path.write_text("[]\n", encoding="utf-8")
        return
    path.write_text("\n".join(entry.rstrip() for entry in entries) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote a simple candidate cross reference after explicit user approval.")
    parser.add_argument("memory_dir", help=".vehicle-embedded-docs directory")
    parser.add_argument("crossref_id", help="Candidate crossref id")
    parser.add_argument("--scope", choices=["portable", "project", "legacy"], default="project", help="Crossref scope to promote from")
    parser.add_argument("--approved-by", required=True, help="Name or note for explicit user approval")
    args = parser.parse_args()

    memory = Path(args.memory_dir).resolve()
    if args.scope == "portable":
        crossref_dir = memory / "portable" / "crossrefs"
    elif args.scope == "legacy":
        crossref_dir = memory / "crossrefs"
    else:
        crossref_dir = memory / "project" / "crossrefs"
    candidate_path = crossref_dir / "candidate-links.yml"
    verified_path = crossref_dir / "verified-links.yml"

    candidate_text = candidate_path.read_text(encoding="utf-8", errors="replace") if candidate_path.exists() else "[]\n"
    verified_text = verified_path.read_text(encoding="utf-8", errors="replace") if verified_path.exists() else "[]\n"

    candidates = split_entries(candidate_text)
    verified = split_entries(verified_text)

    match = None
    remaining = []
    for entry in candidates:
        if scalar(entry, "id") == args.crossref_id:
            match = entry
        else:
            remaining.append(entry)

    if match is None:
        raise SystemExit(f"candidate not found: {args.crossref_id}")
    if not has_evidence(match):
        raise SystemExit("cannot promote without evidence")
    if args.scope == "portable" and mentions_project_only(match):
        raise SystemExit("cannot promote portable crossref that mentions project/code-only material")

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    match = replace_or_add(match, "status", "verified")
    match = replace_or_add(match, "portability", args.scope if args.scope != "legacy" else "project")
    match = replace_or_add(match, "verified_by_user", "true")
    match = replace_or_add(match, "verified_at", f'"{now}"')
    match = replace_or_add(match, "approved_by", f'"{args.approved_by}"')

    verified.append(match)
    write_entries(candidate_path, remaining)
    write_entries(verified_path, verified)
    print(f"promoted: {args.crossref_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
