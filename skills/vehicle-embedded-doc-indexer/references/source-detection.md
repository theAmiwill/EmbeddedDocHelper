# Source Detection

Classify files conservatively. If unsure, use `unknown` and explain what extra evidence is needed.

Every source should receive:

- `source_class`: `hardware`, `software`, `code`, or `unknown`.
- `type`: more specific source type.
- `portability`: `portable` or `project`.
- `authority_role`: `hardware_primary`, `software_guide`, or `code_context_only`.

## PDF Types

Use these signals:

- Schematic: title blocks, sheet numbers, reference designators, nets, connectors, symbols, many short pages.
- Datasheet: electrical characteristics, package, pin description, absolute maximum ratings, short-to-medium length.
- Reference manual: chapters for peripherals, registers, clocks, reset, interrupts, very large page count.
- User manual/application note: board operation, example circuits, setup flow, software notes.
- Errata: defect lists, workaround tables, device revisions.
- Software/tool guide: DaVinci, MCAL, BSW, AUTOSAR module, configuration workflow, generated files, parameter reference.

## Hardware Sources

Default to `source_class: hardware` and `authority_role: hardware_primary` for:

- Chip reference manuals, datasheets, user manuals, errata, and application notes.
- Project schematics and vendor evaluation-board schematics.
- Pinout, pin mux, register, electrical, clock, reset, interrupt, and package material.

Portability:

- Chip and vendor hardware manuals are usually `portable`.
- Project board schematics are usually `project`.
- Vendor evaluation-board schematics are `portable` only when the user says they are reusable reference material.

## Software Sources

Default to `source_class: software` and `authority_role: software_guide` for:

- DaVinci Configurator, EB tresos, MCAL, BSW, AUTOSAR, RTE, diagnostic, bootloader, and toolchain manuals.
- Configuration workflow documents, generated-code guides, module integration manuals, and parameter references.

Software manuals are usually `portable` when the same tool/vendor/version/module set is reused across projects.

Use `software_subtype` to preserve useful relationships inside software sources:

- `tool_guide`: EB Studio, DaVinci, tresos, configurator, or IDE/tool user/developer guides.
- `autosar_standard`: AUTOSAR standard material or AUTOSAR requirement extracts.
- `vendor_requirement`: vendor requirement extracts that are not AUTOSAR standard extracts.
- `vendor_mcal_manual`: MCAL driver user manuals and module user manuals.
- `build_install_guide`: build, installation, integration, or setup guides.
- `demo_app_guide`: DemoApp or example application guides.
- `software_general`: software source that does not fit a narrower subtype.

Do not collapse these subtypes away. Curator may build candidate cross references between software subtypes, for example AUTOSAR requirement extract -> vendor requirement extract -> MCAL UM -> tool guide.

## Excel Types

Use workbook/sheet names, headers, and key columns:

- Pin mux: pin, port, alternate function, ball, package.
- Register export: address, register, bit, reset value, access type.
- BOM: designator, part number, value, package.
- Requirement/config table: module, parameter, variant, value.
- Signal matrix: net, connector, MCU pin, direction, voltage.

## Code Sources

Default to `source_class: code`, `portability: project`, and `authority_role: code_context_only` for:

- Demo projects supplied by vendors.
- Known-good projects named by the user.
- Current project code and generated configuration files.

Only index code paths explicitly named by the user. Do not auto-scan the whole project as a code source. Code helps locate examples and project structure, but cannot prove hardware/software correctness.

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
