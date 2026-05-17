---
name: vehicle-embedded-doc-indexer
description: Build or refresh project-local indexes for vehicle embedded engineering documents. Use when Codex needs to ingest schematics, chip manuals, datasheets, reference manuals, PDF attachments, or Excel attachments for automotive/embedded/BSW/driver work; create `.vehicle-embedded-docs/`, add it to `.gitignore`, summarize document structure, and avoid re-scanning large PDFs when an index already exists.
---

# Vehicle Embedded Doc Indexer

## Purpose

Create a reusable, project-local document memory at `.vehicle-embedded-docs/` for vehicle embedded projects. Prefer factual indexes over design conclusions: record what each source contains, where relevant sections are, and how to locate evidence later.

Default to engineering-location-first output with a brief beginner explanation after each conclusion.

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
   - Rebuild only when source files changed, the index is missing/corrupt, or the user explicitly requests a rebuild.

4. Inventory sources.
   - Record file path, type, size, modified time, hash, page/sheet count when practical.
   - Use `scripts/hash_sources.py` for stable file fingerprints.
   - Classify sources as schematic, manual, datasheet, reference manual, attachment, or unknown.
   - See `references/source-detection.md` for classification rules.

5. Index by source type.
   - Schematics: index sheets/pages, module names, ICs, connectors, power domains, clocks, resets, buses, key nets, MCU pins, and test points. See `references/schematic-indexing.md`.
   - Manuals: first extract table of contents/bookmarks/intro and build chapter trees with page ranges; do not read huge manuals end-to-end. See `references/manual-indexing.md`.
   - Attachments: catalog workbooks, sheets, header rows, key columns, and likely links to manuals/schematics. See `references/attachment-indexing.md`.

6. Write structured files using the schema in `references/index-schema.md`.
   - Write factual indexes to `schematics/`, `manuals/`, and `attachments/`.
   - Put uncertain relationships in `crossrefs/candidate-links.yml`.
   - Leave `crossrefs/verified-links.yml` for the curator skill after evidence and user approval.

7. Report concise status.
   - List sources indexed/refreshed/skipped.
   - Mention any OCR/scanned PDF limitations, missing attachments, ambiguous source types, or source/index conflicts.
   - Include next recommended queries.

## Required Directory Layout

Create this layout when missing:

```text
.vehicle-embedded-docs/
  README.md
  manifest.yml
  sources.yml
  schematics/
  manuals/
  attachments/
  crossrefs/
    candidate-links.yml
    verified-links.yml
    conflicts.yml
  features/
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
- If source evidence conflicts, write the conflict instead of forcing a conclusion.
- Do not add `.vehicle-embedded-docs/` to Git; keep it ignored by default.

## Evidence Standard

Every useful index entry should point back to source evidence:

- PDF: file path plus PDF page number; also include drawing sheet number if printed on the schematic.
- Excel: file path plus sheet name and row/column range when known.
- Manual chapter: file path, chapter title, and page range.
- Inference: mark as `candidate` and include confidence.

## Related Skill

Use `vehicle-embedded-doc-curator` after this skill when answering specific engineering questions, correcting indexes, adding cross references, or writing verified feature-oriented knowledge.
