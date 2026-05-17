# Query Routing

Start every answer by routing the user request to the narrowest evidence path.

## Common Routes

Schematic location:

- Read `schematics/*/sheets.yml`.
- Open relevant PDF pages only.

Signal trace:

- Read `nets.yml`, `sheets.yml`, and relevant schematic pages.
- Check components/connectors around the signal.

Pin/function lookup:

- Combine schematic MCU pin evidence, manual pin/port function tables, and pin mux Excel attachments.

Manual section lookup:

- Read `manuals/*/outline.yml`.
- Open the smallest relevant chapter/page range.

Register/peripheral lookup:

- Read manual outline and any `register-map.yml`.
- Confirm register naming conventions before interpreting bitfields.

Attachment/table lookup:

- Read `attachments/*/catalog.yml`.
- Open only relevant workbook sheets and rows.

MCAL/BSW impact:

- Gather evidence for pins, clock, reset, interrupts, peripheral instance, electrical constraints, and board connection.
- Map to likely AUTOSAR modules only after evidence exists.

Feature bring-up:

- Create or update `features/<feature-id>.md`.
- Use verified links when available; label candidates clearly.

## Default Output

Use:

```text
Conclusion
Evidence
Reasoning
Beginner explanation
Uncertainty
Next checks
```
