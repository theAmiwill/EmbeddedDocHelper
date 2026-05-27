---
name: vehicle-embedded-doc-indexer
description: Build or refresh layered, project-local indexes for vehicle embedded engineering sources. Use when Codex needs to ingest or reuse hardware documents, software manuals, explicit demo/known-good code projects, schematics, chip manuals, datasheets, reference manuals, PDF/Excel attachments, DaVinci/MCAL/BSW/tool guides, or code context for automotive embedded work; create `.vehicle-embedded-docs/`, add it to `.gitignore`, maintain portable hardware/software packages separately from project-local code, and avoid re-scanning large sources when reusable indexes already exist.
---

# Vehicle Embedded Doc Indexer

## Purpose

Create a reusable, layered memory at `.vehicle-embedded-docs/` for vehicle embedded projects. Prefer factual indexes over design conclusions: record what each source contains, where relevant sections are, what can be reused across projects, and how to locate evidence later.

Default to engineering-location-first output with a brief beginner explanation after each conclusion.

## Source Model

Use three source classes:

- Hardware: chip manuals, datasheets, reference manuals, vendor hardware guides, reusable evaluation-board schematics, and project schematics. Treat as the primary correctness basis.
- Software: DaVinci, MCAL, BSW, toolchain, configuration, and vendor software guides. Treat as operating/configuration guidance.
- Code: explicit demo projects, known-good projects, or current project code. Treat as context and fast location aid only; never use code as correctness evidence.

Split indexes by portability:

- `portable/`: reusable hardware/software packages and their hardware-software cross references.
- `project/`: project schematics, explicit code projects, project-specific links, project features, and project lessons.

## Workflow

1. Locate the project root.
   - Use the current working directory unless the user names another project path.
   - Treat `.vehicle-embedded-docs/manifest.yml` as the existing memory marker.

2. Ensure local memory is ignored by Git.
   - Run `scripts/ensure_gitignore.py <project-root>`.
   - Only append `.vehicle-embedded-docs/`; do not sort, rewrite, or clean `.gitignore`.

3. Create or reuse `.vehicle-embedded-docs/`.
   - Run `scripts/ensure_memory_dir.py <project-root>`.
   - If `manifest.yml` exists, perform a brief refresh check before doing any expensive extraction.
   - Support old v1 memory by adding the v2 `portable/` and `project/` layout without deleting old files.
   - Rebuild only when source files changed, the index is missing/corrupt, or the user explicitly requests a rebuild.

4. Reuse portable packages first.
   - Scan `.vehicle-embedded-docs/portable/**/package.yml` before opening large PDFs.
   - Run `scripts/check_portable_packages.py <project-root>`.
   - Match reusable packages by declared identity plus source fingerprints: chip/software name, vendor, version, package/variant, source hash, page count, or sheet list.
   - If a package matches, reuse its outline, sections, attachments, and portable cross references. Only fill missing or stale pieces.
   - See `references/portable-packages.md`.

5. Inventory new or missing sources.
   - Record file path, type, size, modified time, hash, page/sheet count when practical.
   - Use `scripts/hash_sources.py` for stable file fingerprints.
   - Classify sources by source class, source type, portability, and authority role.
   - See `references/source-detection.md` for classification rules.

6. Index by source class and type.
   - Hardware schematics: index sheets/pages, module names, ICs, connectors, power domains, clocks, resets, buses, key nets, MCU pins, and test points. See `references/schematic-indexing.md`.
   - Hardware manuals: extract table of contents/bookmarks/intro and build chapter trees with page ranges; do not read huge manuals end-to-end. See `references/manual-indexing.md`.
   - Software manuals: index tool workflows, module chapters, configuration parameters, generated-file notes, and warnings. See `references/software-indexing.md`.
   - Attachments: catalog workbooks, sheets, header rows, key columns, and likely links to hardware/software sections. See `references/attachment-indexing.md`.
   - Code projects: index only explicit paths named by the user. Record structure, likely modules, config files, generated files, and entry points. See `references/code-indexing.md`.

7. Write structured files using the schema in `references/index-schema.md`.
   - Put portable hardware indexes under `portable/hardware/<package-id>/`.
   - Put portable software indexes under `portable/software/<package-id>/`.
   - Put project schematics and code indexes under `project/`.
   - Put reusable hardware-software links in `portable/crossrefs/`.
   - Put any link involving code, current project paths, current board schematics, or project assumptions in `project/crossrefs/`.
   - Leave verified links for the curator skill after source validation and user approval.

8. Report concise status.
   - List sources indexed/refreshed/skipped.
   - List portable packages reused and why they matched.
   - Mention any OCR/scanned PDF limitations, missing attachments, ambiguous source types, or source/index conflicts.
   - Include next recommended queries.

## Required Directory Layout

Create the v2 layout when missing. Keep legacy v1 files if they already exist.

```text
.vehicle-embedded-docs/
  README.md
  manifest.yml
  sources.yml
  portable/
    hardware/
    software/
    crossrefs/
      candidate-links.yml
      verified-links.yml
      conflicts.yml
    features/
      index.yml
    lessons/
      index.yml
  project/
    sources.yml
    schematics/
    code/
    crossrefs/
      candidate-links.yml
      verified-links.yml
      conflicts.yml
    features/
      index.yml
    lessons/
      index.yml
  audit/
    changes.yml
    stale-sources.yml
```

## Memory Policy

- Treat `.vehicle-embedded-docs/` as the cross-conversation memory.
- Never rely on hidden chat history for source knowledge that should persist.
- Prefer small, source-backed YAML entries over long prose.
- Keep first-pass content factual. Avoid asserting implementation decisions unless directly supported by sources.
- Do not let code context override hardware or software documentation.
- Do not put code/project-specific links into portable cross references.
- If source evidence conflicts, write the conflict instead of forcing a conclusion.
- Do not add `.vehicle-embedded-docs/` to Git; keep it ignored by default.

## Evidence Standard

Every useful index entry should point back to source evidence:

- PDF: file path plus PDF page number; also include drawing sheet number if printed on the schematic.
- Excel: file path plus sheet name and row/column range when known.
- Manual chapter: file path, chapter title, and page range.
- Code: file path and symbol/config region when known; mark as `code_context_only`.
- Inference: mark as `candidate` and include confidence.

## Related Skill

Use `vehicle-embedded-doc-curator` after this skill when answering specific engineering questions, correcting indexes, adding cross references, or writing verified feature-oriented knowledge.
