#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree


MEMORY_DIR = ".vehicle-embedded-docs"
DOC_EXTENSIONS = {".pdf", ".xlsx", ".xlsm", ".xls", ".csv", ".tsv", ".md", ".txt"}
SKIP_DIRS = {".git", ".vehicle-embedded-docs", "node_modules", "__pycache__", "build", "out", "dist", "target"}
MODULE_HINTS = [
    "Adc",
    "Bfx",
    "Bmc",
    "Can",
    "CanIf",
    "CanTp",
    "Com",
    "Crc",
    "Dio",
    "Dma",
    "Eth",
    "Gpt",
    "Icu",
    "Irq",
    "Lin",
    "Mcu",
    "Ocu",
    "Port",
    "Pwm",
    "RvLib",
    "Spi",
    "TInfra",
    "Wdg",
    "Wdg_17_AvWdt",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def stable_id(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "source"


def quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_head(path: Path, size: int = 2_000_000) -> bytes:
    with path.open("rb") as fh:
        return fh.read(size)


def pdf_page_count(path: Path) -> int | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    # This is an approximation that works for many PDFs when no PDF library is available.
    count = len(re.findall(rb"/Type\s*/Page\b", data))
    return count or None


def text_hint(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt", ".csv", ".tsv"}:
        return path.read_text(encoding="utf-8", errors="replace")[:20_000]
    if suffix == ".pdf":
        raw = read_head(path)
        return raw.decode("latin-1", errors="ignore")[:20_000]
    return ""


def module_hints(path: Path, text: str) -> list[str]:
    haystack = f"{path.as_posix()}\n{text}"
    found = []
    for module in MODULE_HINTS:
        if re.search(rf"(^|[^A-Za-z0-9]){re.escape(module)}([^A-Za-z0-9]|$)", haystack, re.IGNORECASE):
            found.append(module)
    return sorted(set(found))


def software_subtype(path: Path, text: str) -> str | None:
    name = path.as_posix().upper()
    haystack = f"{name}\n{text}".upper()
    if "BUILD_INSTALLATION" in name or "BUILD-INSTALLATION" in name or "BUILD INSTALLATION" in name or "INSTALLATION" in name:
        return "build_install_guide"
    if "DEMOAPP" in name or "DEMO_APP" in name or "DEMO APP" in name or "DEMO APPLICATION" in name:
        return "demo_app_guide"
    if "AUTOSAR" in name or re.search(r"R\d{2}[-_ ]?\d{2}", name):
        return "autosar_standard"
    if "REQ_EXTRACT" in name or "REQ-EXTRACT" in name or "REQ EXTRACT" in name:
        return "vendor_requirement"
    if "MCAL" in name or "DRIVERS_UM" in name or "_UM_" in name or "_UM." in name or "USER MANUAL" in name:
        return "vendor_mcal_manual"
    if re.search(r"\b(EB|STUDIO|DAVINCI|TRESOS|CONFIGURATOR)\b", name) or "CONFIGURATION TOOL" in name:
        return "tool_guide"
    if "BUILD_INSTALLATION" in haystack or "BUILD-INSTALLATION" in haystack or "BUILD INSTALLATION" in haystack or "INSTALLATION" in haystack:
        return "build_install_guide"
    if "DEMOAPP" in haystack or "DEMO_APP" in haystack or "DEMO APP" in haystack or "DEMO APPLICATION" in haystack:
        return "demo_app_guide"
    if "REQ_EXTRACT" in haystack or "REQ-EXTRACT" in haystack or "REQ EXTRACT" in haystack:
        return "vendor_requirement"
    if "MCAL" in haystack or "DRIVERS_UM" in haystack or "_UM_" in haystack or "_UM." in haystack or "USER MANUAL" in haystack:
        return "vendor_mcal_manual"
    if "AUTOSAR" in haystack or re.search(r"R\d{2}[-_ ]?\d{2}", haystack):
        return "autosar_standard"
    if re.search(r"\b(EB|STUDIO|DAVINCI|TRESOS|CONFIGURATOR)\b", haystack) or "CONFIGURATION TOOL" in haystack:
        return "tool_guide"
    if re.search(r"\b(BSW|RTE|CONFIGURATION|GENERATED FILES?)\b", haystack):
        return "software_general"
    return None


def classify(path: Path, text: str) -> dict:
    haystack = f"{path.as_posix()}\n{text}".upper()
    suffix = path.suffix.lower()
    subtype = software_subtype(path, text)
    if suffix in {".xlsx", ".xlsm", ".xls", ".csv", ".tsv"}:
        return {
            "source_class": "attachment",
            "type": "attachment",
            "portability": "portable",
            "authority_role": "software_guide" if subtype else "hardware_primary",
            "software_subtype": subtype,
        }
    if subtype:
        return {
            "source_class": "software",
            "type": "software_manual",
            "portability": "portable",
            "authority_role": "software_guide",
            "software_subtype": subtype,
        }
    if "SCHEMATIC" in haystack or "原理图" in haystack or "CIRCUIT" in haystack:
        return {
            "source_class": "hardware",
            "type": "schematic",
            "portability": "project",
            "authority_role": "hardware_primary",
            "software_subtype": None,
        }
    if "DATASHEET" in haystack or "REFERENCE MANUAL" in haystack or "USER'S MANUAL" in haystack or "HARDWARE" in haystack:
        return {
            "source_class": "hardware",
            "type": "reference_manual",
            "portability": "portable",
            "authority_role": "hardware_primary",
            "software_subtype": None,
        }
    return {
        "source_class": "unknown",
        "type": "unknown",
        "portability": "project",
        "authority_role": "hardware_primary",
        "software_subtype": None,
    }


def iter_sources(paths: list[Path]):
    for raw in paths:
        path = raw.resolve()
        if path.is_file() and path.suffix.lower() in DOC_EXTENSIONS:
            yield path
            continue
        if path.is_dir():
            for item in path.rglob("*"):
                if any(part in SKIP_DIRS for part in item.parts):
                    continue
                if item.is_file() and item.suffix.lower() in DOC_EXTENSIONS:
                    yield item


def xlsx_sheet_names(path: Path) -> list[str]:
    if path.suffix.lower() not in {".xlsx", ".xlsm"}:
        return []
    try:
        with zipfile.ZipFile(path) as zf:
            data = zf.read("xl/workbook.xml")
    except (KeyError, OSError, zipfile.BadZipFile):
        return []
    root = ElementTree.fromstring(data)
    names = []
    for elem in root.iter():
        if elem.tag.endswith("sheet") and "name" in elem.attrib:
            names.append(elem.attrib["name"])
    return names


def source_record(path: Path, root: Path) -> dict:
    hint = text_hint(path)
    info = classify(path, hint)
    stat = path.stat()
    record = {
        "source_id": stable_id(path.stem),
        "source_class": info["source_class"],
        "type": info["type"],
        "portability": info["portability"],
        "authority_role": info["authority_role"],
        "path": rel(path, root),
        "sha256": sha256(path),
        "size_bytes": stat.st_size,
        "modified_at": datetime.fromtimestamp(stat.st_mtime, timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "title_guess": path.stem,
        "module_hints": module_hints(path, hint),
    }
    if info["software_subtype"]:
        record["software_subtype"] = info["software_subtype"]
    if path.suffix.lower() == ".pdf":
        record["page_count_estimate"] = pdf_page_count(path)
    if path.suffix.lower() in {".xlsx", ".xlsm"}:
        record["sheet_names"] = xlsx_sheet_names(path)
    return record


def yaml_scalar(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(quote(str(item)) for item in value) + "]"
    return quote(str(value))


def yaml_mapping(mapping: dict, indent: int = 0) -> str:
    lines = []
    pad = " " * indent
    for key, value in mapping.items():
        lines.append(f"{pad}{key}: {yaml_scalar(value)}")
    return "\n".join(lines) + "\n"


def write_index(memory: Path, record: dict) -> str:
    source_id = record["source_id"]
    source_class = record["source_class"]
    source_type = record["type"]
    if source_class == "software":
        base = memory / "portable" / "software" / source_id / "manuals" / source_id
    elif source_class == "hardware" and source_type == "schematic":
        base = memory / "project" / "schematics" / source_id
    elif source_class == "hardware":
        base = memory / "portable" / "hardware" / source_id / "manuals" / source_id
    elif source_class == "attachment":
        base = memory / "portable" / "software" / source_id / "attachments" / source_id
    else:
        base = memory / "project" / "unknown" / source_id
    base.mkdir(parents=True, exist_ok=True)

    if source_class == "attachment":
        target = base / "catalog.yml"
        content = dict(record)
        content["catalog_status"] = "sheet-list-only" if record.get("sheet_names") else "metadata-only"
    elif source_type == "schematic":
        target = base / "index.yml"
        content = dict(record)
        content["index_status"] = "metadata-only"
        content["next_indexing_step"] = "Inspect schematic pages and add sheets.yml, nets.yml, and components.yml."
    else:
        target = base / "outline.yml"
        content = dict(record)
        content["outline_status"] = "metadata-only"
        content["next_indexing_step"] = "Extract PDF bookmarks/table of contents or inspect relevant chapters before using as verified evidence."
    target.write_text(yaml_mapping(content), encoding="utf-8")
    return rel(target, memory)


def append_sources(memory: Path, records: list[dict]) -> None:
    path = memory / "sources.yml"
    existing = path.read_text(encoding="utf-8", errors="replace") if path.exists() else "[]\n"
    existing_ids = set(re.findall(r"(?m)^\s*(?:-\s*)?source_id:\s*['\"]?([^'\"\s]+)", existing))
    if existing.strip() == "[]":
        lines = []
    else:
        lines = [existing.rstrip()]
    for record in records:
        if record["source_id"] in existing_ids:
            continue
        lines.append("- " + f"source_id: {yaml_scalar(record['source_id'])}")
        for key in ("source_class", "type", "portability", "authority_role", "path", "sha256", "size_bytes", "modified_at", "index_path"):
            lines.append(f"  {key}: {yaml_scalar(record.get(key))}")
        if record.get("software_subtype"):
            lines.append(f"  software_subtype: {yaml_scalar(record['software_subtype'])}")
        if record.get("module_hints"):
            lines.append(f"  module_hints: {yaml_scalar(record['module_hints'])}")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def append_project_sources(memory: Path, records: list[dict]) -> None:
    project_records = [record for record in records if record["portability"] == "project"]
    if not project_records:
        return
    path = memory / "project" / "sources.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8", errors="replace") if path.exists() else "[]\n"
    existing_ids = set(re.findall(r"(?m)^\s*(?:-\s*)?source_id:\s*['\"]?([^'\"\s]+)", existing))
    lines = [] if existing.strip() == "[]" else [existing.rstrip()]
    for record in project_records:
        if record["source_id"] in existing_ids:
            continue
        lines.append("- " + f"source_id: {yaml_scalar(record['source_id'])}")
        for key in ("source_class", "type", "portability", "authority_role", "path", "index_path"):
            lines.append(f"  {key}: {yaml_scalar(record.get(key))}")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_audit(memory: Path, records: list[dict]) -> None:
    audit = memory / "audit" / "index-sources-report.json"
    audit.parent.mkdir(parents=True, exist_ok=True)
    audit.write_text(json.dumps({"generated_at": now_utc(), "sources_indexed": records}, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create lightweight non-empty indexes for document source files without third-party dependencies.")
    parser.add_argument("project_root", help="Project root containing .vehicle-embedded-docs")
    parser.add_argument("paths", nargs="+", help="Source files or directories to index")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    memory = project_root / MEMORY_DIR
    if not (memory / "manifest.yml").exists():
        raise SystemExit(f"missing memory directory; run ensure_memory_dir.py first: {memory}")

    records = []
    seen_paths = set()
    for source in iter_sources([Path(raw) for raw in args.paths]):
        source_key = str(source.resolve()).lower()
        if source_key in seen_paths:
            continue
        seen_paths.add(source_key)
        record = source_record(source, project_root)
        record["index_path"] = write_index(memory, record)
        records.append(record)

    append_sources(memory, records)
    append_project_sources(memory, records)
    write_audit(memory, records)
    print(json.dumps({"memory_dir": str(memory), "indexed": len(records)}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
