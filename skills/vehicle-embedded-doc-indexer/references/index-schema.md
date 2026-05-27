# Index Schema

Use `.vehicle-embedded-docs/` as the project-local memory root. Schema v2 separates reusable knowledge from project-specific knowledge.

## Authority Roles

Use these values consistently:

- `hardware_primary`: hardware facts and correctness basis.
- `software_guide`: tool, MCAL, BSW, configuration, or workflow guidance.
- `code_context_only`: code location and project context only; not correctness evidence.

## Top Level

`manifest.yml`:

```yaml
schema_version: 2
created_at: "2026-05-17T00:00:00Z"
updated_at: "2026-05-17T00:00:00Z"
project_root: "."
memory_policy:
  git_tracking: ignored
  verified_requires_user_approval: true
  portable_mode: project-local-copy
authority_order:
  - hardware_primary
  - software_guide
  - code_context_only
sources: []
portable_packages: []
```

`sources.yml` keeps all known sources for quick refresh checks:

```yaml
- source_id: rh850-u2b-reference-manual
  source_class: hardware
  type: reference_manual
  portability: portable
  authority_role: hardware_primary
  path: docs/RH850_U2B.pdf
  sha256: ...
  size_bytes: 0
  modified_at: "2026-05-17T00:00:00Z"
  page_count: 12000
  index_path: portable/hardware/rh850-u2b/manuals/rh850-u2b-reference-manual/outline.yml
  notes: []
```

`project/sources.yml` records project-only sources:

```yaml
- source_id: demo-project
  source_class: code
  type: known_good_project
  portability: project
  authority_role: code_context_only
  path: vendor/demo
  index_path: project/code/demo-project/index.yml
  notes:
    - "Code is context only; do not use as correctness evidence."
```

## Portable Packages

Each reusable package has `package.yml`.

Hardware package:

```yaml
package_id: rh850-u2b-hardware
package_class: hardware
portability: portable
authority_role: hardware_primary
identity:
  vendor: Renesas
  family: RH850
  part_number: RH850/U2B
  package: LQFP
  revision: Rev.1.00
source_fingerprints:
  - source_id: rh850-u2b-reference-manual
    sha256: ...
    page_count: 12000
reusable_scope:
  - chip-manual-outline
  - pin-function-tables
  - clock-reset-register-sections
```

Software package:

```yaml
package_id: davinci-mcal-guide
package_class: software
portability: portable
authority_role: software_guide
identity:
  vendor: Vector
  product: DaVinci Configurator
  module_set: MCAL/BSW
  version: "..."
source_fingerprints:
  - source_id: davinci-guide
    sha256: ...
    page_count: 800
reusable_scope:
  - tool-workflow
  - module-configuration-guide
  - generated-file-notes
```

## Portable Hardware

`portable/hardware/<package-id>/manuals/<manual-id>/outline.yml`:

```yaml
source_id: rh850-u2b-reference-manual
title: "RH850/U2B User's Manual"
outline_status: partial
authority_role: hardware_primary
sections:
  - section_id: clock-generator
    title: "Clock Generator"
    level: 1
    pdf_page_start: 421
    pdf_page_end: 508
    keywords: [clock, pll, oscillator, divider]
```

Reusable schematics, such as vendor evaluation-board schematics, may live under `portable/hardware/<package-id>/schematics/`. Project board schematics should normally live under `project/schematics/`.

## Portable Software

`portable/software/<package-id>/manuals/<manual-id>/outline.yml`:

```yaml
source_id: davinci-mcal-guide
title: "DaVinci MCAL Configuration Guide"
outline_status: partial
authority_role: software_guide
sections:
  - section_id: can-configuration
    title: "CAN Configuration"
    pdf_page_start: 210
    pdf_page_end: 260
    modules: [Can, CanIf]
    keywords: [controller, baudrate, hardware object]
```

Use denser `sections.yml` only after inspecting a chapter.

## Project Schematics

`project/schematics/<schematic-id>/sheets.yml`:

```yaml
- sheet_id: sheet-12
  pdf_page: 12
  drawing_sheet: "12/42"
  title: "CAN Transceiver"
  modules: [CAN, power]
  components: [U12, J3]
  key_nets: [CAN0_TX, CAN0_RX, CANH, CANL]
  authority_role: hardware_primary
  evidence:
    - file: docs/main_board.pdf
      pdf_page: 12
```

## Project Code

`project/code/<code-id>/index.yml`:

```yaml
source_id: demo-project
source_path: vendor/demo
source_class: code
type: known_good_project
portability: project
authority_role: code_context_only
summary: "Explicitly supplied demo project for navigation context."
config_files:
  - path: Config/Can.arxml
    kind: arxml
source_roots:
  - path: Source
    languages: [c, h]
likely_modules:
  - module: Can
    evidence:
      - path: Config/Can.arxml
```

## Cross References

Portable cross references may link only portable hardware and portable software knowledge:

```yaml
- id: link-can0-hardware-software-guide
  status: candidate
  portability: portable
  relation: "CAN0 hardware facts map to reusable CAN configuration guide sections."
  confidence: medium
  evidence:
    - source: portable/hardware/rh850-u2b/manuals/rh850-u2b-reference-manual/outline.yml
      ref: "can-controller"
    - source: portable/software/davinci-mcal-guide/manuals/davinci-guide/outline.yml
      ref: "can-configuration"
  verified_by_user: false
```

Project cross references must be used for anything involving code paths, current project schematics, board variants, local configuration files, or project assumptions:

```yaml
- id: link-can0-project-code
  status: candidate
  portability: project
  relation: "Current project CAN0 configuration appears near Config/Can.arxml."
  authority_role: code_context_only
  evidence:
    - source: project/code/demo-project/index.yml
      ref: "Config/Can.arxml"
  verified_by_user: false
```

Only the curator skill should promote candidate entries to verified links.
