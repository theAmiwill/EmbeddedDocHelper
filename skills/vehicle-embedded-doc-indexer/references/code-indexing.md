# Code Indexing

Code sources are for context and navigation speed. They do not prove the configuration is correct.

## Scope

Index only code directories explicitly named by the user, such as:

- Vendor demo projects.
- Known-good projects.
- Current project folders selected for review.

Do not auto-scan the whole repository as a code source.

## What To Capture

Record:

- Source root paths.
- Configuration files (`.arxml`, `.xml`, `.cfg`, `.ini`, `.json`, `.yaml`, `.yml`).
- Likely MCAL/BSW modules based on filenames and directories.
- Generated code directories.
- Main/source entry points when obvious.
- Build/config scripts when relevant.

## Authority

Always use:

```yaml
authority_role: code_context_only
portability: project
```

Code evidence may support statements like "the current project appears to configure CAN here." It must not support statements like "this CAN configuration is correct."

## Suggested Output

Use `scripts/catalog_code_project.py <project-root> <code-path> --id <code-id>` to generate a lightweight JSON catalog, then translate useful parts into:

```text
project/code/<code-id>/index.yml
```

Keep code indexes small. Prefer paths and module hints over copied code.
