# Repository Instructions

This repository may use EmbeddedDocHelper for vehicle embedded engineering document work.

When asked about schematics, chip manuals, datasheets, reference manuals, Excel attachments, software manuals, explicit code projects, BSW, MCAL, driver bring-up, board bring-up, pins, registers, or peripheral configuration:

- Prefer source-backed answers over memory or guesses.
- Use `.vehicle-embedded-docs/` as the project-local document memory when it exists.
- Treat `.vehicle-embedded-docs/portable/` as reusable hardware/software knowledge and `.vehicle-embedded-docs/project/` as project schematics, code context, local links, features, and lessons.
- On first use, create candidate cross references from existing indexes before relying on the memory as complete.
- If `.vehicle-embedded-docs/` is missing, propose creating it before answering broad document navigation questions.
- Cite evidence with file path, PDF page or schematic sheet, and Excel sheet/row/column where applicable.
- Treat hardware documents as the correctness basis, software documents as configuration guides, and code as context-only navigation data.
- Separate facts from inference.
- Treat new relationships as candidate links until verified by source evidence and explicit user approval.
- For engineering conclusions, answer with conclusion, evidence, reasoning, short beginner explanation, uncertainty, and next checks.

Do not commit `.vehicle-embedded-docs/`; it is local memory and should be ignored by Git.
