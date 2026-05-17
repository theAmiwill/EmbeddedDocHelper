# Crossref Lifecycle

Cross references are the controlled "self-evolution" mechanism.

## Statuses

`candidate`: plausible relation found during a query.

`needs-review`: relation has evidence but conflicts or missing details remain.

`verified`: relation is source-backed, rechecked, and explicitly approved by the user.

`rejected`: relation was investigated and found wrong.

## Candidate Entry

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
  created_from_query: "Confirm CAN0 MCAL configuration evidence path"
  verified_by_user: false
```

## Promotion Requirements

Promote only when all are true:

- The relation has at least one direct source reference.
- The relevant source pages/sheets were re-opened or otherwise rechecked.
- Any conflict has been resolved or recorded.
- The user explicitly approved the conclusion.

Use `scripts/promote_crossref.py` if the YAML is simple and PyYAML is installed; otherwise edit manually and preserve evidence.
