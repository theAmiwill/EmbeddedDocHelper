# Source Detection

Classify files conservatively. If unsure, use `unknown` and explain what extra evidence is needed.

## PDF Types

Use these signals:

- Schematic: title blocks, sheet numbers, reference designators, nets, connectors, symbols, many short pages.
- Datasheet: electrical characteristics, package, pin description, absolute maximum ratings, short-to-medium length.
- Reference manual: chapters for peripherals, registers, clocks, reset, interrupts, very large page count.
- User manual/application note: board operation, example circuits, setup flow, software notes.
- Errata: defect lists, workaround tables, device revisions.

## Excel Types

Use workbook/sheet names, headers, and key columns:

- Pin mux: pin, port, alternate function, ball, package.
- Register export: address, register, bit, reset value, access type.
- BOM: designator, part number, value, package.
- Requirement/config table: module, parameter, variant, value.
- Signal matrix: net, connector, MCU pin, direction, voltage.

## Source IDs

Generate stable lowercase IDs:

- Base on file stem.
- Replace spaces and punctuation with hyphens.
- Append type only when needed to avoid collisions.
- Keep IDs stable after the first index; do not rename casually.

## Refresh Signals

Treat a source as stale when any of these changes:

- SHA-256 hash.
- File size.
- Modified timestamp and hash cannot be computed.
- Page count or workbook sheet list.
- User reports a known wrong mapping.
