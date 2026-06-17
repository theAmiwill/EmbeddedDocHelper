---
name: vehicle-embedded-doc-curator
description: Reuse and evolve layered `.vehicle-embedded-docs/` memory for vehicle embedded engineering questions. Use after `vehicle-embedded-doc-indexer` has created portable hardware/software indexes and project-local code/schematic indexes; answer schematic/manual/software-guide/code-location questions, rely on a capable PDF retrieval skill when PDF evidence must be inspected, correct stale indexes, add evidence-backed portable or project cross references, promote user-approved links, and maintain feature or lesson knowledge for automotive embedded, BSW, MCAL, driver, and board bring-up work.
---

# Vehicle Embedded Doc Curator

Answer concrete engineering questions from `.vehicle-embedded-docs/`, then improve that memory when new evidence appears. Default to engineering-location-first answers with a short beginner explanation.

## Core Rules

- Require `.vehicle-embedded-docs/manifest.yml`; otherwise ask the user to run `vehicle-embedded-doc-indexer` first.
- Authority order is fixed: `hardware_primary` proves correctness, `software_guide` explains configuration/operation, and `code_context_only` only locates examples or project structure.
- Never promote a relationship to `verified` without source validation and explicit user approval.
- Put reusable hardware/software links in `portable/crossrefs/`; put links involving code, project paths, board variants, or local assumptions in `project/crossrefs/`.
- If PDF retrieval is weak, ask for a capable PDF skill such as Anthropic's official `skills/pdf` instead of guessing from metadata.

## Workflow

1. Locate memory with `scripts/find_memory_dir.py <start-path>`.
2. On first use, run `scripts/bootstrap_crossrefs.py <memory-dir>` when `audit/crossref-bootstrap.yml` is absent or crossref files are empty. See `references/bootstrap-crossrefs.md` for bootstrap behavior.
3. Route the query using `references/query-routing.md`.
4. Gather narrow evidence from relevant indexes first, then only the needed PDF pages, Excel sheets, schematic sheets, or code excerpts.
5. Answer with: conclusion, evidence, reasoning, beginner explanation, uncertainty, and next checks. Compress this shape for trivial questions, but keep evidence visible.
6. Repair stale memory when evidence contradicts it; record changes and conflicts under the appropriate portable/project audit or crossref file.
7. Add new relationships as `candidate`; validate existing links with `scripts/validate_crossrefs.py`.
8. For user-approved relationship promotion, use `scripts/promote_crossref.py` when appropriate.
9. For feature paths or lessons, use `references/feature-doc-template.md` and `references/lesson-template.md`.

## Verification Rules

Separate extracted facts from inference, cite source locations for engineering claims, state confidence when evidence is partial, and preserve the hardware/software/code authority model. Do not use demo/current code as proof that a configuration is correct.

Use `vehicle-embedded-doc-indexer` first when memory is absent, stale, or missing important source files.
