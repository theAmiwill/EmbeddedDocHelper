#!/usr/bin/env python3
import argparse
from pathlib import Path


MEMORY_DIR = ".vehicle-embedded-docs"


def main() -> int:
    parser = argparse.ArgumentParser(description="Find .vehicle-embedded-docs by walking upward from a start path.")
    parser.add_argument("start_path", nargs="?", default=".", help="Starting file or directory")
    args = parser.parse_args()

    start = Path(args.start_path).resolve()
    current = start if start.is_dir() else start.parent
    for candidate in [current, *current.parents]:
        memory = candidate / MEMORY_DIR
        if (memory / "manifest.yml").exists():
            print(memory)
            return 0
    print(f"not found: {MEMORY_DIR}", flush=True)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
