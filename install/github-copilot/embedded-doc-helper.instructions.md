---
applyTo: "**/*"
---

# EmbeddedDocHelper Workflow

Use this workflow for vehicle embedded document questions involving schematics, chip manuals, datasheets, reference manuals, Excel attachments, BSW, MCAL, drivers, board bring-up, pins, registers, peripheral configuration, or feature implementation paths.

## Indexing Behavior

If `.vehicle-embedded-docs/` does not exist, recommend creating it before doing broad document analysis. It should contain factual indexes for source documents and must be ignored by Git.

If `.vehicle-embedded-docs/` exists, read it first and avoid repeating expensive full-document scans.

## Answering Behavior

Use this answer shape unless the question is trivial:

```text
Conclusion
Evidence
Reasoning
Beginner explanation
Uncertainty
Next checks
```

## Evidence Rules

- Cite PDF file path and page number.
- For schematics, include printed sheet ID when available.
- For Excel, cite workbook, sheet, and row/column region when available.
- Do not infer MCAL/BSW configuration from a schematic alone.
- Do not promote candidate relationships to verified without source validation and explicit user approval.
