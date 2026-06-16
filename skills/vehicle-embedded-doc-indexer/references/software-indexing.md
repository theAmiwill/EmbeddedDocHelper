# Software Indexing

Software sources explain how to operate tools and configure MCAL/BSW. They are guides, not hardware correctness evidence.

Run `scripts/index_sources.py <project-root> <software-manual-folder>` before manual deep reading. The script creates non-empty source-level indexes and records `software_subtype` when it can infer it from filenames or text snippets.

## What To Capture

For each software manual or guide, record:

- Tool/vendor/product/version.
- `software_subtype` when it can be inferred.
- AUTOSAR or vendor module names.
- Configuration workflows.
- Parameter reference sections.
- Generated file descriptions.
- Warnings, constraints, and known pitfalls.
- Links to relevant hardware facts when directly supported.

## Common Source Types

- DaVinci Configurator guides.
- EB tresos guides.
- MCAL module user manuals.
- BSW integration guides.
- AUTOSAR module references.
- Vendor application notes that describe configuration steps.

## Software Subtypes

Prefer these subtype values:

- `tool_guide`: EB Studio, DaVinci, tresos, configurator, or IDE/tool guides.
- `autosar_standard`: AUTOSAR standard material or AUTOSAR requirement extracts.
- `vendor_requirement`: vendor MCAL/driver requirement extracts.
- `vendor_mcal_manual`: MCAL driver user manuals and module user manuals.
- `build_install_guide`: build, installation, integration, or setup guides.
- `demo_app_guide`: DemoApp or example application guides.
- `software_general`: fallback for software manuals with unclear subtype.

These subtypes are used by curator bootstrap to create software-to-software candidate cross references.

## Index Shape

Use `portable/software/<package-id>/manuals/<manual-id>/outline.yml` for first-pass outlines.

Use `sections.yml` only after inspecting a chapter:

```yaml
- section_id: can-controller-configuration
  title: "CAN Controller Configuration"
  module: Can
  software_subtype: vendor_mcal_manual
  pdf_page_start: 210
  pdf_page_end: 236
  authority_role: software_guide
  parameters: [CanControllerId, CanCpuClockRef, CanControllerBaudrateConfig]
  generated_files: [Can_Cfg.c, Can_Cfg.h]
  evidence:
    - file: docs/davinci_mcal_guide.pdf
      pdf_page: 210
```

## Limits

- Do not use software manuals to prove a board connection exists.
- Do not use software manuals to prove a pin mux is valid; check hardware manuals and pin tables.
- When software instructions conflict with hardware facts, record the conflict and prefer hardware facts.
