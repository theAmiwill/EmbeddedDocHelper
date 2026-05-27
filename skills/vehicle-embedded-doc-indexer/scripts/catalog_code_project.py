#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


CONFIG_EXTENSIONS = {".arxml", ".xml", ".cfg", ".ini", ".json", ".yaml", ".yml"}
SOURCE_EXTENSIONS = {".c", ".h"}
SCRIPT_EXTENSIONS = {".bat", ".ps1", ".mak", ".mk"}
SKIP_DIRS = {".git", ".vehicle-embedded-docs", "node_modules", "__pycache__", "build", "out", "dist", "target"}
MODULE_HINTS = [
    "Adc",
    "Can",
    "CanIf",
    "CanTp",
    "Com",
    "Dio",
    "Eth",
    "Gpt",
    "Lin",
    "Mcu",
    "Pwm",
    "Port",
    "Spi",
    "Wdg",
]


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def iter_files(root: Path, max_files: int):
    count = 0
    for path in root.rglob("*"):
        if count >= max_files:
            break
        if should_skip(path) or not path.is_file():
            continue
        count += 1
        yield path


def module_hints(path: Path) -> list[str]:
    text = path.as_posix()
    found = []
    for module in MODULE_HINTS:
        if re.search(rf"(^|[^A-Za-z]){re.escape(module)}([^A-Za-z]|$)", text, re.IGNORECASE):
            found.append(module)
    return sorted(set(found))


def main() -> int:
    parser = argparse.ArgumentParser(description="Catalog an explicitly supplied code project as context-only navigation data.")
    parser.add_argument("project_root", help="Project root for relative paths")
    parser.add_argument("code_path", help="Explicit code/demo/known-good project directory")
    parser.add_argument("--id", dest="source_id", help="Stable source id for this code project")
    parser.add_argument("--max-files", type=int, default=5000, help="Maximum files to inspect")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    code_root = Path(args.code_path).resolve()
    if not code_root.exists():
        raise SystemExit(f"missing code path: {args.code_path}")
    if not code_root.is_dir():
        raise SystemExit(f"code path must be a directory: {args.code_path}")

    source_id = args.source_id or re.sub(r"[^a-z0-9]+", "-", code_root.name.lower()).strip("-") or "code-project"
    config_files = []
    source_files = []
    build_scripts = []
    modules = {}

    for path in iter_files(code_root, args.max_files):
        suffix = path.suffix.lower()
        rel_path = rel(path, project_root)
        hints = module_hints(path)
        for module in hints:
            modules.setdefault(module, []).append(rel_path)

        if suffix in CONFIG_EXTENSIONS:
            config_files.append({"path": rel_path, "kind": suffix.lstrip("."), "module_hints": hints})
        elif suffix in SOURCE_EXTENSIONS:
            source_files.append({"path": rel_path, "kind": suffix.lstrip("."), "module_hints": hints})
        elif suffix in SCRIPT_EXTENSIONS or path.name.lower() in {"makefile", "cmakelists.txt"}:
            build_scripts.append({"path": rel_path, "kind": path.name})

    result = {
        "source_id": source_id,
        "source_path": rel(code_root, project_root),
        "source_class": "code",
        "type": "explicit_code_project",
        "portability": "project",
        "authority_role": "code_context_only",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "summary": "Context-only code catalog. Do not use as correctness evidence.",
        "config_files": config_files[:200],
        "source_files_sample": source_files[:200],
        "build_scripts": build_scripts[:100],
        "likely_modules": [
            {"module": module, "example_paths": paths[:10]}
            for module, paths in sorted(modules.items())
        ],
        "limits": {
            "max_files": args.max_files,
            "config_files_truncated": len(config_files) > 200,
            "source_files_truncated": len(source_files) > 200,
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
