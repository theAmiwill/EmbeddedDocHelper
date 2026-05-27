#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


MEMORY_DIR = ".vehicle-embedded-docs"


def scalar(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*(.+?)\s*$", text)
    if not match:
        return None
    return match.group(1).strip().strip('"').strip("'")


def package_record(package_path: Path, memory: Path) -> dict:
    text = package_path.read_text(encoding="utf-8", errors="replace")
    issues = []
    package_id = scalar(text, "package_id")
    package_class = scalar(text, "package_class")
    authority_role = scalar(text, "authority_role")
    portability = scalar(text, "portability")

    if not package_id:
        issues.append("missing package_id")
    if package_class not in {"hardware", "software"}:
        issues.append(f"unexpected package_class: {package_class!r}")
    if portability != "portable":
        issues.append("portability must be portable")
    if authority_role not in {"hardware_primary", "software_guide"}:
        issues.append(f"unexpected authority_role: {authority_role!r}")
    if "identity:" not in text:
        issues.append("missing identity")
    if "source_fingerprints:" not in text:
        issues.append("missing source_fingerprints")

    return {
        "path": str(package_path.relative_to(memory)).replace("\\", "/"),
        "package_id": package_id,
        "package_class": package_class,
        "authority_role": authority_role,
        "portability": portability,
        "reusable": not issues,
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="List portable hardware/software packages copied into a project memory directory.")
    parser.add_argument("project_root", help="Project root or .vehicle-embedded-docs directory")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    memory = root if root.name == MEMORY_DIR else root / MEMORY_DIR
    portable = memory / "portable"
    records = []
    if portable.exists():
        for package_path in sorted(portable.glob("*/*/package.yml")):
            records.append(package_record(package_path, memory))

    print(json.dumps({"memory_dir": str(memory), "portable_packages": records}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
