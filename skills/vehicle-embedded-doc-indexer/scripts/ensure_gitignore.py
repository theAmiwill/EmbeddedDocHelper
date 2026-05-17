#!/usr/bin/env python3
import argparse
from pathlib import Path


RULE = ".vehicle-embedded-docs/"


def main() -> int:
    parser = argparse.ArgumentParser(description="Ensure the local vehicle embedded document memory is gitignored.")
    parser.add_argument("project_root", help="Project root directory")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    gitignore = root / ".gitignore"

    if gitignore.exists():
        text = gitignore.read_text(encoding="utf-8", errors="replace")
        lines = [line.strip() for line in text.splitlines()]
        if RULE in lines:
            print(f"already ignored: {RULE}")
            return 0
        prefix = "" if text.endswith(("\n", "\r")) or text == "" else "\n"
        gitignore.write_text(text + prefix + RULE + "\n", encoding="utf-8")
        print(f"appended to .gitignore: {RULE}")
        return 0

    gitignore.write_text(RULE + "\n", encoding="utf-8")
    print(f"created .gitignore with: {RULE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
