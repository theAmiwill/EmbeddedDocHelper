# Index Schema

Use `.vehicle-embedded-docs/` as the project-local memory root.

## Top Level

`manifest.yml`:

```yaml
schema_version: 1
created_at: "2026-05-17T00:00:00Z"
updated_at: "2026-05-17T00:00:00Z"
project_root: "."
memory_policy:
  git_tracking: ignored
  verified_requires_user_approval: true
sources:
  - source_id: main-schematic
    type: schematic
    path: docs/board.pdf
    sha256: ...
    status: indexed
```

`sources.yml` keeps one entry per source:

```yaml
- source_id: rh850-u2b-reference-manual
  type: reference_manual
  path: docs/RH850_U2B.pdf
  sha256: ...
  size_bytes: 0
  modified_at: "2026-05-17T00:00:00Z"
  page_count: 12000
  index_path: manuals/rh850-u2b-reference-manual/outline.yml
  notes: []
```

## Schematics

`schematics/<schematic-id>/index.yml`:

```yaml
source_id: main-schematic
source_path: docs/main_board.pdf
pdf_page_count: 42
status: partial
summary: "Main board schematic with MCU, power, CAN, LIN, and connectors."
```

`sheets.yml`:

```yaml
- sheet_id: sheet-12
  pdf_page: 12
  drawing_sheet: "12/42"
  title: "CAN Transceiver"
  modules: [CAN, power]
  components: [U12, J3]
  key_nets: [CAN0_TX, CAN0_RX, CANH, CANL]
  evidence:
    - file: docs/main_board.pdf
      pdf_page: 12
```

## Manuals

`manuals/<manual-id>/outline.yml`:

```yaml
source_id: rh850-u2b-reference-manual
title: "RH850/U2B User's Manual"
outline_status: partial
sections:
  - section_id: clock-generator
    title: "Clock Generator"
    level: 1
    pdf_page_start: 421
    pdf_page_end: 508
    keywords: [clock, pll, oscillator, divider]
```

Use `sections.yml` for denser extracted notes when a chapter is actually inspected.

## Attachments

`attachments/<attachment-id>/catalog.yml`:

```yaml
source_id: pinmux-excel
source_path: docs/pinmux.xlsx
workbook_type: xlsx
sheets:
  - name: PinMux
    rows: 2200
    columns: 35
    header_guess: 3
    key_columns: [Pin, Port, Alternate Function]
    likely_links:
      - manual_section: port-function
        confidence: medium
```

## Cross References

Put unverified links in `crossrefs/candidate-links.yml`:

```yaml
- id: link-can0-port-pinmux
  status: candidate
  relation: "CAN0 schematic nets likely map to MCU alternate pin functions."
  confidence: medium
  evidence:
    - source: schematics/main-board/sheets.yml
      ref: "sheet-12"
    - source: manuals/rh850-u2b/outline.yml
      ref: "port-function"
  verified_by_user: false
```

Only the curator skill should promote entries to `crossrefs/verified-links.yml`.
