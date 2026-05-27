# Lesson Template

Use lessons for reusable cautions, pitfalls, and experience discovered during project work.

## Location

Use `portable/lessons/` when the lesson applies across projects using the same hardware/software package and does not mention local code paths.

Use `project/lessons/` when the lesson depends on:

- Current project code.
- Current board schematics or wiring.
- Local configuration files.
- Debug process or project-specific constraints.

## Template

```markdown
# <Lesson Title>

## Portability
portable or project, with the reason.

## Applies To
Hardware package, software package, project, module, or feature.

## Lesson
The concise takeaway.

## Evidence
- Source-backed references or project observations.

## Validation
How this was checked, and whether the user approved it.

## Related Links
- Crossrefs, features, source indexes, or code indexes.

## Open Questions
- Anything not yet verified.
```

Do not use lessons to bypass evidence rules. Lessons can guide future searches, but engineering conclusions still need source evidence.
