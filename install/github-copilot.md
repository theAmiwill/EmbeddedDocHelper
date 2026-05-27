# Install for GitHub Copilot

GitHub Copilot does not use local Agent Skill folders the same way Codex, Claude Code, and Kilo Code do. For Copilot, install repository instructions that describe the same workflow.

## Project Install

```powershell
.\scripts\install-github-copilot.ps1 -TargetProject C:\path\to\your\project
```

macOS/Linux:

```sh
./scripts/install-github-copilot.sh /path/to/your/project
```

This creates or updates:

```text
.github/copilot-instructions.md
.github/instructions/embedded-doc-helper.instructions.md
```

The repository-wide file gives Copilot broad guidance. The path-specific instruction file applies the EmbeddedDocHelper workflow across the repository, including the portable/project split and the hardware/software/code authority model.

## Manual Install

Copy:

```text
install/github-copilot/copilot-instructions.md
```

to:

```text
.github/copilot-instructions.md
```

Copy:

```text
install/github-copilot/embedded-doc-helper.instructions.md
```

to:

```text
.github/instructions/embedded-doc-helper.instructions.md
```

If your target project already has `.github/copilot-instructions.md`, merge the EmbeddedDocHelper section instead of overwriting the file.
