# Bootstrap Cross References

Run this on the first curator use for a project memory so the user starts with a candidate relationship map.

## Trigger

Bootstrap when either is true:

- `audit/crossref-bootstrap.yml` is missing.
- `portable/crossrefs/*` and `project/crossrefs/*` have no candidate or verified entries.

Do not bootstrap repeatedly on every question. After a run, write `audit/crossref-bootstrap.yml`.

## Behavior

Use existing index files only. Do not reopen large PDFs or rescan full code projects during bootstrap.

Generate only `candidate` entries:

- Portable candidates: relations between `portable/hardware/` and `portable/software/`.
- Software-internal candidates: relations between reusable software subtypes such as AUTOSAR standard extracts, vendor requirement extracts, MCAL user manuals, EB/DaVinci/tool guides, DemoApp guides, and build/install guides.
- Project candidates: any relation involving `project/`, code indexes, project schematics, local config, or board-specific evidence.

Default confidence should be `low` unless the same specific module/peripheral identifier appears in both sources. Use `medium` for direct module terms such as `CAN0`, `SPI2`, `ADC`, `Port`, `Mcu`, or explicit matching section IDs.

For software-internal bootstrap, prefer these candidate chains:

- AUTOSAR standard or AUTOSAR requirement extract -> vendor requirement extract.
- Vendor requirement extract -> MCAL user manual.
- MCAL user manual -> EB/DaVinci/tool guide.
- MCAL user manual -> DemoApp or build/install guide.

If there is no specific module overlap but the subtype relation is obvious, generate only a low-confidence software-stack candidate.

## Output

Write to:

- `portable/crossrefs/candidate-links.yml`
- `project/crossrefs/candidate-links.yml`
- `audit/crossref-bootstrap.yml`

Each candidate must include:

- `id`
- `status: candidate`
- `portability`
- `relation`
- `confidence`
- `evidence`
- `created_from_query: "Initial curator crossref bootstrap"`
- `verified_by_user: false`

## Review

Before using generated candidates as reasoning support:

- Run `scripts/validate_crossrefs.py <memory-dir>`.
- Treat bootstrap candidates as search hints, not conclusions.
- Promote only after reopening or rechecking the cited source evidence and receiving explicit user approval.
