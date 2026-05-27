# Query Routing

Start every answer by routing the user request to the narrowest evidence path. Prefer indexes before original source files.

## Default Three-Source Flow

For feature or configuration questions, gather in this order:

1. Hardware facts: what the chip, board, pin, peripheral, clock, reset, interrupt, and electrical evidence says.
2. Software guidance: where the tool or MCAL/BSW manual explains the operation or configuration.
3. Code context: where the current/demo/known-good project appears to implement or configure it.

Use code only for location and context.

## Common Routes

Hardware location:

- Read `portable/hardware/*` for reusable chip/vendor manuals.
- Read `project/schematics/*` for current board schematics.
- Open relevant PDF pages only.

Signal trace:

- Read project `nets.yml`, `sheets.yml`, and relevant schematic pages.
- Check components/connectors around the signal.
- Link to portable chip pin/function tables only after matching pins or nets.

Pin/function lookup:

- Combine schematic MCU pin evidence, portable manual pin/port function tables, and pin mux Excel attachments.
- Only then consult software guide sections for configuration steps.

Software guide lookup:

- Read `portable/software/*/manuals/*/outline.yml`.
- Open the smallest relevant guide chapter/page range.
- Treat findings as operating instructions, not proof of hardware facts.

Register/peripheral lookup:

- Read portable hardware manual outline and any register map.
- Confirm register naming conventions before interpreting bitfields.

Attachment/table lookup:

- Read package attachment catalogs.
- Open only relevant workbook sheets and rows.

Code location:

- Read `project/code/*/index.yml`.
- Use source excerpts only after indexes identify likely files.
- Mark conclusions as `code_context_only`.

MCAL/BSW impact:

- Gather hardware facts for pins, clock, reset, interrupts, peripheral instance, electrical constraints, and board connection.
- Gather software guide sections for module workflow and parameter names.
- Gather code locations for current implementation only if the user provided explicit code sources.
- Put links involving code into `project/crossrefs/`.

Feature bring-up:

- Create or update `portable/features/<feature-id>.md` for reusable hardware/software paths.
- Create or update `project/features/<feature-id>.md` when code paths, project schematics, or local configuration are involved.
- Use verified links when available; label candidates clearly.

Lesson capture:

- Put reusable cautions in `portable/lessons/`.
- Put project-specific debugging notes in `project/lessons/`.

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
