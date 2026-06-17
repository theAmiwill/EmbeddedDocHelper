---
name: vehicle-embedded-doc-curator
description: Reuse and evolve layered `.vehicle-embedded-docs/` memory for vehicle embedded engineering questions. Use after `vehicle-embedded-doc-indexer` has created portable hardware/software indexes and project-local code/schematic indexes; answer schematic/manual/software-guide/code-location questions, correct stale indexes, add evidence-backed portable or project cross references, promote user-approved links, and maintain feature or lesson knowledge for automotive embedded, BSW, MCAL, driver, and board bring-up work.
---

# Vehicle Embedded Doc Curator

## Purpose

Answer concrete engineering questions from the layered memory in `.vehicle-embedded-docs/`, then improve that memory when new evidence appears. Keep the system conservative: candidate relationships can be added freely with evidence; verified knowledge requires source validation and explicit user approval.

Default to engineering-location-first output with a brief beginner explanation after each conclusion.

## Authority Model

Use this evidence priority:

1. `hardware_primary`: chip manuals, datasheets, reference manuals, schematics, pin tables, electrical/clock/reset/register facts.
2. `software_guide`: DaVinci, MCAL, BSW, AUTOSAR, and tool manuals that explain operations and configuration.
3. `code_context_only`: explicit demo/current/known-good code used only to locate implementation examples and project structure.

Never treat code as proof that a configuration is correct. If hardware, software, and code disagree, prefer hardware facts and record the conflict.

## Preconditions

1. Find `.vehicle-embedded-docs/manifest.yml` from the current project root.
2. If it does not exist, stop and ask the user to run `vehicle-embedded-doc-indexer` first.
3. Read `README.md`, `manifest.yml`, `sources.yml`, and only the relevant portable/project index files for the current question.

Use `scripts/find_memory_dir.py <start-path>` to locate the memory directory.

## Workflow

1. Bootstrap candidate cross references on first use.
   - If `audit/crossref-bootstrap.yml` is absent, or both portable/project crossref files are empty, generate initial `candidate` cross references from existing indexes before answering.
   - Prefer `scripts/bootstrap_crossrefs.py <memory-dir>` for a deterministic first pass.
   - Include software-internal candidates when AUTOSAR extracts, vendor requirements, MCAL manuals, EB/DaVinci/tool guides, DemoApp guides, or build/install guides share modules or software-stack context.
   - Review generated candidates for obvious false positives; keep them as unverified and low/medium confidence.
   - See `references/bootstrap-crossrefs.md`.

2. Route the query.
   - Classify the user request as hardware location, signal trace, pin/function lookup, software guide lookup, register/peripheral lookup, attachment/table lookup, code location, MCAL/BSW impact, feature bring-up, or lesson capture.
   - See `references/query-routing.md`.

3. Gather narrow evidence.
   - Start from index files.
   - Read portable hardware/software indexes before opening large source files.
   - Read project code indexes only for location and context.
   - Open only relevant PDF pages, manual chapters, Excel sheets, or code excerpts.
   - Do not rescan full manuals unless the index is missing and the user approves a rebuild.

4. Answer with the standard format.
   - Conclusion
   - Evidence
   - Reasoning
   - Beginner explanation
   - Uncertainty
   - Next checks

5. Repair memory when evidence contradicts it.
   - Correct wrong page ranges, missing sheets, wrong module names, stale source metadata, or mistaken links.
   - Record changes in `audit/changes.yml`.
   - Put unresolved portable contradictions in `portable/crossrefs/conflicts.yml`.
   - Put project/code/local contradictions in `project/crossrefs/conflicts.yml`.

6. Add cross references carefully.
   - Reusable hardware-software relationships go to `portable/crossrefs/candidate-links.yml`.
   - Any relation involving code, project paths, current board schematics, local configuration, or board variants goes to `project/crossrefs/candidate-links.yml`.
   - Use `scripts/validate_crossrefs.py` before trusting existing links.
   - Promote only after repeated source validation and explicit user approval. See `references/crossref-lifecycle.md`.

7. Maintain feature knowledge.
   - When the user asks for a function-oriented path, create or update `portable/features/<feature-id>.md` or `project/features/<feature-id>.md` based on portability.
   - Include only verified or clearly labeled candidate knowledge.
   - Use `references/feature-doc-template.md`.

8. Maintain lessons.
   - Put portable lessons in `portable/lessons/` only when they do not depend on code paths or project-specific board details.
   - Put project lessons in `project/lessons/` when they mention local configuration, code, board wiring, or debugging process.
   - Use `references/lesson-template.md`.

## Verification Rules

- A relation is not verified just because it sounds plausible.
- Require source references for every engineering conclusion.
- Separate facts from inference.
- State confidence when evidence is partial.
- Ask for user approval before promoting any candidate link to verified.
- Do not promote portable links that mention `project/`, `code/`, project file paths, or current board assumptions.

## Response Style

Keep answers pragmatic and source-grounded. Prefer:

```text
Conclusion: ...
Evidence: ...
Reasoning: ...
Beginner explanation: ...
Uncertainty: ...
Next checks: ...
```

For simple questions, compress this into short paragraphs but keep evidence visible.

## Related Skill

Use `vehicle-embedded-doc-indexer` first when `.vehicle-embedded-docs/` is absent, stale, or missing important source files.
