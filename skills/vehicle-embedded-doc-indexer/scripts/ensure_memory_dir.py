#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone
from pathlib import Path


MEMORY_DIR = ".vehicle-embedded-docs"


FILES = {
    "README.md": """# Vehicle Embedded Docs

Project-local memory for schematics, chip manuals, datasheets, attachments, cross references, and verified feature knowledge.

Use `vehicle-embedded-doc-indexer` to create or refresh factual indexes.
Use `vehicle-embedded-doc-curator` to answer questions, correct indexes, and promote verified relationships.
""",
    "sources.yml": "[]\n",
    "crossrefs/candidate-links.yml": "[]\n",
    "crossrefs/verified-links.yml": "[]\n",
    "crossrefs/conflicts.yml": "[]\n",
    "features/index.yml": "[]\n",
    "audit/changes.yml": "[]\n",
    "audit/stale-sources.yml": "[]\n",
}


DIRS = [
    "schematics",
    "manuals",
    "attachments",
    "crossrefs",
    "features",
    "audit",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the .vehicle-embedded-docs skeleton without overwriting existing files.")
    parser.add_argument("project_root", help="Project root directory")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    memory = root / MEMORY_DIR
    memory.mkdir(parents=True, exist_ok=True)

    for rel in DIRS:
        (memory / rel).mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    manifest = memory / "manifest.yml"
    if not manifest.exists():
        manifest.write_text(
            "\n".join(
                [
                    "schema_version: 1",
                    f'created_at: "{now}"',
                    f'updated_at: "{now}"',
                    'project_root: "."',
                    "memory_policy:",
                    "  git_tracking: ignored",
                    "  verified_requires_user_approval: true",
                    "sources: []",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    for rel, content in FILES.items():
        target = memory / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_text(content, encoding="utf-8")

    print(memory)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
