# Software Indexing

Software sources explain how to operate tools and configure MCAL/BSW. They are guides, not hardware correctness evidence.

## What To Capture

For each software manual or guide, record:

- Tool/vendor/product/version.
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

## Index Shape

Use `portable/software/<package-id>/manuals/<manual-id>/outline.yml` for first-pass outlines.

Use `sections.yml` only after inspecting a chapter:

```yaml
- section_id: can-controller-configuration
  title: "CAN Controller Configuration"
  module: Can
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
