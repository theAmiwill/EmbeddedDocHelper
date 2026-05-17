# Evidence Policy

The memory directory is useful only if it stays trustworthy.

## Evidence Levels

Fact:

- Directly visible in a source.
- Has file path plus page/sheet/row reference.

Inference:

- Derived from multiple facts.
- Must include reasoning and confidence.

Candidate cross reference:

- Plausible relation with evidence but not yet user-approved.

Verified cross reference:

- Source-backed, rechecked, and explicitly approved by the user.

## Required Citations

PDF evidence:

- File path.
- PDF page number.
- Printed sheet or chapter when available.

Excel evidence:

- File path.
- Sheet name.
- Row/column or table region when available.

Index evidence:

- Index file path.
- Entry ID.
- Original source references.

## Prohibited Moves

- Do not promote a candidate because it is useful.
- Do not treat a schematic net as proof of pin mux configuration.
- Do not treat a manual peripheral chapter as proof that the board uses that peripheral.
- Do not hide conflicts. Record them in `crossrefs/conflicts.yml`.
