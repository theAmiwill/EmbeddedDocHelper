---
name: vehicle-embedded-doc-indexer
description: Build or refresh layered, project-local indexes for vehicle embedded engineering sources. Use when Codex needs to ingest or reuse hardware documents, software manuals, explicit demo/known-good code projects, schematics, chip manuals, datasheets, reference manuals, PDF/Excel attachments, DaVinci/MCAL/BSW/tool guides, or code context for automotive embedded work; create `.vehicle-embedded-docs/`, add it to `.gitignore`, rely on a capable PDF retrieval skill when PDFs must be inspected, maintain portable hardware/software packages separately from project-local code, and avoid re-scanning large sources when reusable indexes already exist.
---

# Vehicle Embedded Doc Indexer

Create or refresh `.vehicle-embedded-docs/` as reusable, project-local document memory. Keep first-pass content factual: describe what each source is, where evidence can be found, and what can be reused later. Default to engineering-location-first output plus a short beginner explanation.

## Core Rules

- Treat hardware documents as correctness evidence, software documents as configuration/operation guides, and code as context-only navigation.
- Split reusable hardware/software knowledge under `portable/`; keep project schematics, code, local links, features, and lessons under `project/`.
- Do not put code paths, current-board assumptions, or project-only schematics into portable cross references.
- For PDFs, use native PDF retrieval or an installed PDF skill when reliable; otherwise write `metadata-only` indexes and do not infer technical content.
- Keep `.vehicle-embedded-docs/` ignored by Git.

## Workflow

1. Locate the project root. Treat `.vehicle-embedded-docs/manifest.yml` as the existing memory marker.
2. Run `scripts/ensure_gitignore.py <project-root>` and `scripts/ensure_memory_dir.py <project-root>`.
3. Before opening large PDFs, run `scripts/check_portable_packages.py <project-root>` and reuse matching `portable/**/package.yml` data.
4. Run `scripts/index_sources.py <project-root> <source-path>...` to create lightweight, non-empty source indexes.
5. Classify sources by class, type, portability, and authority role. Read `references/source-detection.md` for ambiguous files.
6. For deeper indexing, read only the relevant reference:
   - Schema/layout: `references/index-schema.md`
   - Portable reuse: `references/portable-packages.md`
   - Hardware manuals: `references/manual-indexing.md`
   - Schematics: `references/schematic-indexing.md`
   - Software manuals: `references/software-indexing.md`
   - Attachments: `references/attachment-indexing.md`
   - Code context: `references/code-indexing.md`
7. Report sources indexed/refreshed/skipped, portable packages reused, metadata-only limits, conflicts, and next recommended checks.

## Evidence Standard

Every useful index entry should point back to source evidence: PDF path/page, schematic sheet, Excel workbook/sheet/row/column, manual chapter/page range, or code path/symbol. Mark inference as `candidate` with confidence.

Use `vehicle-embedded-doc-curator` after indexing when answering engineering questions, correcting indexes, adding cross references, or writing verified feature-oriented knowledge.
