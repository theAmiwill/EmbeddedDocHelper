#!/usr/bin/env python3
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_EXTENSIONS = {
    ".pdf",
    ".xlsx",
    ".xlsm",
    ".xls",
    ".csv",
    ".tsv",
    ".md",
    ".txt",
}


SKIP_DIRS = {".git", ".vehicle-embedded-docs", "node_modules", "__pycache__"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_files(path: Path):
    if path.is_file():
        yield path
        return
    for item in path.rglob("*"):
        if any(part in SKIP_DIRS for part in item.parts):
            continue
        if item.is_file() and item.suffix.lower() in DEFAULT_EXTENSIONS:
            yield item


def file_record(path: Path, root: Path | None) -> dict:
    stat = path.stat()
    display = str(path)
    if root is not None:
        try:
            display = str(path.relative_to(root))
        except ValueError:
            pass
    return {
        "path": display.replace("\\", "/"),
        "size_bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "sha256": sha256(path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Hash source documents for .vehicle-embedded-docs indexes.")
    parser.add_argument("paths", nargs="+", help="Files or directories to fingerprint")
    parser.add_argument("--root", help="Root used for relative output paths")
    args = parser.parse_args()

    root = Path(args.root).resolve() if args.root else None
    records = []
    for raw in args.paths:
        path = Path(raw).resolve()
        if not path.exists():
            records.append({"path": raw, "error": "missing"})
            continue
        for file_path in iter_files(path):
            records.append(file_record(file_path.resolve(), root))

    print(json.dumps(records, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
