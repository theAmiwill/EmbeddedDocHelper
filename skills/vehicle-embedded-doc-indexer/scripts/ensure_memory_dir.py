#!/usr/bin/env python3
import argparse
import re
from datetime import datetime, timezone
from pathlib import Path


MEMORY_DIR = ".vehicle-embedded-docs"


README = """# Vehicle Embedded Docs

Project-local memory for layered vehicle embedded sources.

Use `vehicle-embedded-doc-indexer` to create, refresh, or reuse factual indexes.
Use `vehicle-embedded-doc-curator` to answer questions, correct indexes, and promote verified relationships.

`portable/` contains reusable hardware/software indexes copied between projects.
`project/` contains current-project schematics, code context, cross references, features, and lessons.
"""


FILES = {
    "README.md": README,
    "sources.yml": "[]\n",
    "portable/crossrefs/candidate-links.yml": "[]\n",
    "portable/crossrefs/verified-links.yml": "[]\n",
    "portable/crossrefs/conflicts.yml": "[]\n",
    "portable/features/index.yml": "[]\n",
    "portable/lessons/index.yml": "[]\n",
    "project/sources.yml": "[]\n",
    "project/crossrefs/candidate-links.yml": "[]\n",
    "project/crossrefs/verified-links.yml": "[]\n",
    "project/crossrefs/conflicts.yml": "[]\n",
    "project/features/index.yml": "[]\n",
    "project/lessons/index.yml": "[]\n",
    "audit/changes.yml": "[]\n",
    "audit/stale-sources.yml": "[]\n",
}


DIRS = [
    "portable/hardware",
    "portable/software",
    "portable/crossrefs",
    "portable/features",
    "portable/lessons",
    "project/schematics",
    "project/code",
    "project/crossrefs",
    "project/features",
    "project/lessons",
    "audit",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def create_manifest(path: Path) -> None:
    now = now_utc()
    path.write_text(
        "\n".join(
            [
                "schema_version: 2",
                f'created_at: "{now}"',
                f'updated_at: "{now}"',
                'project_root: "."',
                "memory_policy:",
                "  git_tracking: ignored",
                "  verified_requires_user_approval: true",
                "  portable_mode: project-local-copy",
                "authority_order:",
                "  - hardware_primary",
                "  - software_guide",
                "  - code_context_only",
                "sources: []",
                "portable_packages: []",
                "",
            ]
        ),
        encoding="utf-8",
    )


def upgrade_manifest(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text

    if re.search(r"(?m)^schema_version:\s*1\s*$", text):
        text = re.sub(r"(?m)^schema_version:\s*1\s*$", "schema_version: 2", text)
    elif not re.search(r"(?m)^schema_version:\s*", text):
        text = "schema_version: 2\n" + text

    if "updated_at:" not in text:
        text = re.sub(r"(?m)^(created_at:.*\n)", rf'\1updated_at: "{now_utc()}"\n', text, count=1)

    if "verified_requires_user_approval:" not in text:
        if "memory_policy:" in text:
            text = re.sub(
                r"(?m)^(memory_policy:\n)",
                r"\1  verified_requires_user_approval: true\n",
                text,
                count=1,
            )
        else:
            text += "\nmemory_policy:\n  git_tracking: ignored\n  verified_requires_user_approval: true\n"

    if "portable_mode:" not in text:
        if "memory_policy:" in text:
            text = re.sub(
                r"(?m)^(memory_policy:\n(?:  .+\n)*)",
                r"\1  portable_mode: project-local-copy\n",
                text,
                count=1,
            )
        else:
            text += "\nmemory_policy:\n  git_tracking: ignored\n  verified_requires_user_approval: true\n  portable_mode: project-local-copy\n"

    if "authority_order:" not in text:
        text += "\nauthority_order:\n  - hardware_primary\n  - software_guide\n  - code_context_only\n"
    if "portable_packages:" not in text:
        text += "portable_packages: []\n"

    if text != original:
        path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or upgrade the .vehicle-embedded-docs v2 skeleton without deleting existing files.")
    parser.add_argument("project_root", help="Project root directory")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    memory = root / MEMORY_DIR
    memory.mkdir(parents=True, exist_ok=True)

    for rel in DIRS:
        (memory / rel).mkdir(parents=True, exist_ok=True)

    manifest = memory / "manifest.yml"
    if manifest.exists():
        upgrade_manifest(manifest)
    else:
        create_manifest(manifest)

    for rel, content in FILES.items():
        target = memory / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            target.write_text(content, encoding="utf-8")

    print(memory)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
