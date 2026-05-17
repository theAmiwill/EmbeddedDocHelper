---
name: vehicle-embedded-doc-curator
description: Reuse and evolve `.vehicle-embedded-docs/` for vehicle embedded engineering questions. Use after `vehicle-embedded-doc-indexer` has created project-local document indexes; answer schematic/manual/attachment questions, correct stale indexes, add evidence-backed cross references, promote user-approved links, and maintain feature-oriented knowledge for automotive embedded, BSW, MCAL, driver, and board bring-up work.
---

# Vehicle Embedded Doc Curator

## Purpose

Answer concrete engineering questions from the project-local memory in `.vehicle-embedded-docs/`, then improve that memory when new evidence appears. Keep the system conservative: candidate relationships can be added freely with evidence; verified knowledge requires source validation and explicit user approval.

Default to engineering-location-first output with a brief beginner explanation after each conclusion.

## Preconditions

1. Find `.vehicle-embedded-docs/manifest.yml` from the current project root.
2. If it does not exist, stop and ask the user to run `vehicle-embedded-doc-indexer` first.
3. Read `README.md`, `manifest.yml`, `sources.yml`, and only the relevant index files for the current question.

Use `scripts/find_memory_dir.py <start-path>` to locate the memory directory.

## Workflow

1. Route the query.
   - Classify the user request as schematic location, signal trace, pin/function lookup, manual section lookup, register/peripheral lookup, attachment/table lookup, MCAL/BSW impact, or feature bring-up.
   - See `references/query-routing.md`.

2. Gather narrow evidence.
   - Start from index files.
   - Open only relevant PDF pages, manual chapters, Excel sheets, or source excerpts.
   - Do not rescan full manuals unless the index is missing and the user approves a rebuild.

3. Answer with the standard format.
   - Conclusion
   - Evidence
   - Reasoning
   - Beginner explanation
   - Uncertainty
   - Next checks

4. Repair memory when evidence contradicts it.
   - Correct wrong page ranges, missing sheets, wrong module names, stale source metadata, or mistaken links.
   - Record changes in `audit/changes.yml`.
   - Put unresolved contradictions in `crossrefs/conflicts.yml`.

5. Add cross references carefully.
   - New inferred relationships go to `crossrefs/candidate-links.yml`.
   - Use `scripts/validate_crossrefs.py` before trusting existing links.
   - Promote only after repeated source validation and explicit user approval. See `references/crossref-lifecycle.md`.

6. Maintain feature knowledge.
   - When the user asks for a function-oriented path, create or update `features/<feature-id>.md`.
   - Include only verified or clearly labeled candidate knowledge.
   - Use `references/feature-doc-template.md`.

## Verification Rules

- A relation is not verified just because it sounds plausible.
- Require source references for every engineering conclusion.
- Separate facts from inference.
- State confidence when evidence is partial.
- Ask for user approval before promoting any candidate link to verified.

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
