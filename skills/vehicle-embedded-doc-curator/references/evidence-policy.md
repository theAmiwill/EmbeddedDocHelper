# Evidence Policy

The memory directory is useful only if it stays trustworthy.

## Authority Roles

`hardware_primary`:

- Chip manuals, datasheets, reference manuals, pin tables, register maps, electrical characteristics, clock/reset/interrupt sections, schematics.
- Primary correctness basis.

`software_guide`:

- DaVinci, MCAL, BSW, AUTOSAR, toolchain, and vendor software manuals.
- Explains operations, configuration flows, generated files, and parameter meaning.

`code_context_only`:

- Demo projects, known-good projects, current project code, generated configuration files.
- Helps locate implementation and understand project shape.
- Never proves correctness.

## Evidence Levels

Fact:

- Directly visible in a source.
- Has file path plus page/sheet/row/path reference.

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

Code evidence:

- File path.
- Symbol, config object, or approximate region when known.
- `authority_role: code_context_only`.

Index evidence:

- Index file path.
- Entry ID.
- Original source references.

## Conflict Rules

- Hardware facts outrank software guidance.
- Software guidance outranks code examples.
- Code cannot override hardware or software sources.
- Record unresolved conflicts in `portable/crossrefs/conflicts.yml` or `project/crossrefs/conflicts.yml` based on portability.

## Prohibited Moves

- Do not promote a candidate because it is useful.
- Do not treat a schematic net as proof of pin mux configuration.
- Do not treat a manual peripheral chapter as proof that the board uses that peripheral.
- Do not treat code as proof that a configuration is correct.
- Do not put code or project-specific paths in portable verified links.
- Do not hide conflicts.
