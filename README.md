# EmbeddedDocHelper

EmbeddedDocHelper packages two Agent Skills for vehicle embedded engineering document work:

- `vehicle-embedded-doc-indexer`: creates or refreshes layered `.vehicle-embedded-docs/` memory from portable hardware/software documents and explicit project code sources, including non-empty first-pass source indexes.
- `vehicle-embedded-doc-curator`: reuses `.vehicle-embedded-docs/` to bootstrap first-use candidate links, answer engineering questions, correct stale indexes, maintain evidence-backed portable/project cross references, and write verified feature or lesson notes.

The default workflow is engineering-location-first: find the exact page/sheet/table, cite evidence, then add a short beginner explanation.

Because EmbeddedDocHelper depends heavily on PDF retrieval, installing Anthropic's official [`skills/pdf`](https://github.com/anthropics/skills/tree/main/skills/pdf) alongside these skills is recommended when your agent supports it.

## License

EmbeddedDocHelper is licensed under the GNU Affero General Public License v3.0 only (`AGPL-3.0-only`).

If you use, modify, redistribute, or provide this project as part of a service, preserve the copyright notice, keep the original repository attribution, and comply with the AGPL-3.0-only terms. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

## Repository Layout

```text
skills/
  vehicle-embedded-doc-indexer/
  vehicle-embedded-doc-curator/
install/
  agent-rules/
    embedded-doc-helper.md
  codex.md
  claude-code.md
  kilo-code.md
  github-copilot.md
  github-copilot/
    copilot-instructions.md
scripts/
  install-codex.ps1
  install-claude-code.ps1
  install-kilo-code.ps1
  install-github-copilot.ps1
  install-project-rules.ps1
```

## Quick Install

From a cloned copy of this repository:

```powershell
.\scripts\install-codex.ps1
.\scripts\install-claude-code.ps1
.\scripts\install-kilo-code.ps1
```

To install the skills and also add project-level rules:

```powershell
.\scripts\install-codex.ps1 -TargetProject C:\path\to\your\project
.\scripts\install-claude-code.ps1 -TargetProject C:\path\to\your\project
.\scripts\install-kilo-code.ps1 -TargetProject C:\path\to\your\project
```

On macOS/Linux:

```sh
./scripts/install-codex.sh
./scripts/install-claude-code.sh
./scripts/install-kilo-code.sh
```

Pass the target project path to also install project-level rules:

```sh
./scripts/install-codex.sh /path/to/your/project
./scripts/install-claude-code.sh /path/to/your/project
./scripts/install-kilo-code.sh /path/to/your/project
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
  portable/
  project/
```

`portable/` is meant to be copied between projects when the same chip or software stack is reused. `project/` holds current-project schematics, code context, local cross references, features, and lessons.

The indexer runs a lightweight first pass over supplied source files so manuals and schematics get metadata/outline placeholders even when no PDF parser is available. These entries are marked `metadata-only` until a later targeted deep read confirms chapter details.

It also appends this line to the project `.gitignore`:

```gitignore
.vehicle-embedded-docs/
```

The second skill requires that directory to exist. On first use, it can generate initial candidate cross references from existing indexes so later questions have a relationship map to verify. This includes software-internal links such as AUTOSAR extracts -> vendor requirements -> MCAL user manuals -> EB/DaVinci/tool guides. It treats cross references as a lifecycle:

```text
candidate -> needs-review -> verified -> rejected
```

Only source-backed and explicitly user-approved relationships should become `verified`.

Authority order is fixed: hardware documents are the correctness basis, software documents are operation/configuration guides, and code is context-only navigation data.

## Install Guides

- [Codex](install/codex.md)
- [Claude Code](install/claude-code.md)
- [Kilo Code](install/kilo-code.md)
- [GitHub Copilot](install/github-copilot.md)

Project rule installers write:

```text
Codex:       AGENTS.md
Claude Code: CLAUDE.md
Kilo Code:   .kilocode/rules/embedded-doc-helper.md
Copilot:     .github/copilot-instructions.md
```

## Validation

The skills were validated with `quick_validate.py` using Python plus `PyYAML`. Helper scripts were syntax-checked and smoke-tested on Windows.
