# Feature Document Template

Create feature documents only for function-oriented knowledge the user wants to reuse.

Use:

- `portable/features/<feature-id>.md` for reusable hardware/software paths.
- `project/features/<feature-id>.md` when project schematics, code paths, local configuration, or debugging process are involved.

Use lowercase hyphen IDs such as:

- `can0-bringup`
- `adc-channel-check`
- `spi-device-integration`
- `pwm-output-debug`

Template:

```markdown
# <Feature Name>

## Scope
What function, board area, or software integration this document covers.

## Portability
portable or project, with the reason.

## Hardware Basis
Primary hardware evidence: schematic sheets, chip manual sections, pin mux, clock/reset/interrupt/register facts.

## Software Guide
Tool/MCAL/BSW guide sections, parameter names, generated-file notes, and workflow references.

## Code Context
Project code/config paths only when applicable. Mark as context, not correctness evidence.

## Verified Source Chain
1. Hardware facts.
2. Software guide steps.
3. Project code locations, if applicable.

## Evidence
- Source file, PDF page/sheet, Excel sheet/row, code path, or index entry.

## Confirmed Decisions
- User-approved conclusions only.

## Candidate Links
- Plausible but not yet verified relationships.

## Lessons
- Reusable cautions or project-specific notes linked to `lessons/`.

## Beginner Explanation
Short explanation of the feature path for a new embedded engineer.

## Open Questions
- Missing evidence, unresolved conflicts, or checks still needed.
```

Keep feature documents concise. Link back to verified cross references when possible.
