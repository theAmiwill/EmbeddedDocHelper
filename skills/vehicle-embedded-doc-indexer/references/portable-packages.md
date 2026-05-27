# Portable Packages

Portable packages let a new project reuse indexes copied from another project without re-reading large sources.

## Location

Use project-local copy only:

```text
.vehicle-embedded-docs/portable/
```

Do not search a global library by default. The user should copy reusable package folders from an old project into the new project.

## Package Types

Hardware packages:

- Chip manuals, datasheets, reference manuals, errata, reusable vendor guides.
- Reusable evaluation-board schematics only when explicitly identified as reusable.
- Use `authority_role: hardware_primary`.

Software packages:

- DaVinci, MCAL, BSW, AUTOSAR, toolchain, and vendor software manuals.
- Use `authority_role: software_guide`.

Do not store code projects in portable packages by default.

## Matching Rules

Treat a package as reusable when declaration and fingerprints agree:

- Hardware: vendor, family, part number, package/variant, revision.
- Software: vendor, product/tool name, module set, version.
- Fingerprints: source SHA-256 when available, page count for PDFs, sheet list for workbooks.

If identity matches but fingerprints differ, mark it `needs-review` or stale. Do not silently reuse verified links.

## Reuse Flow

1. Scan `portable/**/package.yml`.
2. Summarize matching packages before opening source PDFs.
3. Reuse existing outlines, sections, attachments, and portable cross references.
4. Fill only missing or stale indexes.
5. Keep new project schematics, code paths, and local configuration in `project/`.

## Cross Reference Boundary

`portable/crossrefs/` may link only portable hardware and portable software.

Move a link to `project/crossrefs/` if it mentions:

- `project/`
- `code/`
- Current project file paths.
- Current board schematics.
- Board-specific wiring, solder options, variants, or local configuration.
