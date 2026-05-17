# Attachment Indexing

Treat Excel attachments as structured evidence, not as secondary notes.

## Workbook Catalog

For each workbook, record:

- File path and hash.
- Workbook type.
- Sheet names.
- Row/column counts.
- Guessed header row.
- Important columns.
- Hidden sheets if detectable.
- Formula presence if relevant.

Use `scripts/catalog_excel.py <workbook>` for `.xlsx` and `.xlsm` files when Python `openpyxl` is available.

## Common Automotive Attachments

- Pin mux tables.
- Register maps.
- Package/ball maps.
- IO signal matrices.
- Board signal lists.
- MCAL configuration exports.
- AUTOSAR parameter tables.
- BOM or variant tables.

## Linking Attachments

Attachment links to manuals/schematics are often inferred. Put these in `candidate-links.yml` unless directly confirmed by matching identifiers and source evidence.

Strong signals:

- Same pin names and package names.
- Same register names and addresses.
- Same peripheral instance names.
- Same net names or connector labels.

Weak signals:

- Similar module names only.
- User memory without source evidence.
- File naming conventions without content confirmation.
