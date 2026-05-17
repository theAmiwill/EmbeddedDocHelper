# EmbeddedDocHelper

EmbeddedDocHelper packages two Agent Skills for vehicle embedded engineering document work:

- `vehicle-embedded-doc-indexer`: creates or refreshes `.vehicle-embedded-docs/` from schematics, chip manuals, datasheets, reference manuals, and Excel attachments.
- `vehicle-embedded-doc-curator`: reuses `.vehicle-embedded-docs/` to answer engineering questions, correct stale indexes, maintain evidence-backed cross references, and write verified feature notes.

The default workflow is engineering-location-first: find the exact page/sheet/table, cite evidence, then add a short beginner explanation.

## Repository Layout

```text
skills/
  vehicle-embedded-doc-indexer/
  vehicle-embedded-doc-curator/
install/
  codex.md
  claude-code.md
  kilo-code.md
  github-copilot.md
  github-copilot/
    copilot-instructions.md
    embedded-doc-helper.instructions.md
scripts/
  install-codex.ps1
  install-claude-code.ps1
  install-kilo-code.ps1
  install-github-copilot.ps1
```

## Quick Install

From a cloned copy of this repository:

```powershell
.\scripts\install-codex.ps1
.\scripts\install-claude-code.ps1
.\scripts\install-kilo-code.ps1
```

On macOS/Linux:

```sh
./scripts/install-codex.sh
./scripts/install-claude-code.sh
./scripts/install-kilo-code.sh
```

For GitHub Copilot repository instructions:

```powershell
.\scripts\install-github-copilot.ps1 -TargetProject C:\path\to\your\project
```

On macOS/Linux:

```sh
./scripts/install-github-copilot.sh /path/to/your/project
```

## Skill Behavior

The first skill creates a project-local memory directory:

```text
.vehicle-embedded-docs/
```

It also appends this line to the project `.gitignore`:

```gitignore
.vehicle-embedded-docs/
```

The second skill requires that directory to exist. It treats cross references as a lifecycle:

```text
candidate -> needs-review -> verified -> rejected
```

Only source-backed and explicitly user-approved relationships should become `verified`.

## Install Guides

- [Codex](install/codex.md)
- [Claude Code](install/claude-code.md)
- [Kilo Code](install/kilo-code.md)
- [GitHub Copilot](install/github-copilot.md)

## Validation

The skills were validated with `quick_validate.py` using Python plus `PyYAML`. Helper scripts were syntax-checked and smoke-tested on Windows.
