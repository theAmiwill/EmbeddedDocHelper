# Feature Document Template

Create feature documents in `features/<feature-id>.md` only for function-oriented knowledge the user wants to reuse.

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

## Verified Source Chain
1. Schematic evidence.
2. Manual chapter evidence.
3. Attachment/table evidence.
4. AUTOSAR/BSW/driver impact evidence.

## Evidence
- Source file, PDF page/sheet, Excel sheet/row, or index entry.

## Confirmed Decisions
- User-approved conclusions only.

## Candidate Links
- Plausible but not yet verified relationships.

## Beginner Explanation
Short explanation of the feature path for a new embedded engineer.

## Open Questions
- Missing evidence, unresolved conflicts, or checks still needed.
```

Keep feature documents concise. Link back to `crossrefs/verified-links.yml` when possible.
