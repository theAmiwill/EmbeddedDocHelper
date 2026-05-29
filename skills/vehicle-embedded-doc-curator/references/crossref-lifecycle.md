# Crossref Lifecycle

Cross references are the controlled self-evolution mechanism.

## Statuses

`candidate`: plausible relation found during a query.

Bootstrap candidates may be generated from existing indexes during first curator use. They are search hints, not conclusions.
Bootstrap may include same-class software relations, such as AUTOSAR requirement extract -> vendor requirement extract -> MCAL user manual -> tool guide.

`needs-review`: relation has evidence but conflicts or missing details remain.

`verified`: relation is source-backed, rechecked, and explicitly approved by the user.

`rejected`: relation was investigated and found wrong.

## Portability

`portable/crossrefs/`:

- Link only portable hardware and portable software knowledge.
- Do not mention code paths, current project paths, project schematics, board variants, or local configuration.

`project/crossrefs/`:

- Use for any relation involving code, current board schematics, current project configuration, local paths, or project-specific assumptions.

## Candidate Entry

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
  created_from_query: "Confirm reusable CAN0 configuration evidence path"
  verified_by_user: false
```

Project-only example:

```yaml
- id: link-can0-project-config
  status: candidate
  portability: project
  authority_role: code_context_only
  relation: "Current project CAN configuration appears near Config/Can.arxml."
  evidence:
    - source: project/code/demo-project/index.yml
      ref: "Config/Can.arxml"
  verified_by_user: false
```

## Promotion Requirements

Promote only when all are true:

- The relation has at least one direct source reference.
- The relevant source pages/sheets/files were re-opened or otherwise rechecked.
- Any conflict has been resolved or recorded.
- The user explicitly approved the conclusion.
- Portable promotions do not mention code or project-specific paths.

Use `scripts/promote_crossref.py --scope portable|project` if the YAML is simple; otherwise edit manually and preserve evidence.
