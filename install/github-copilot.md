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
```

The repository-wide file gives Copilot the EmbeddedDocHelper workflow, including the portable/project split and the hardware/software/code authority model.

Copilot does not necessarily execute local Agent Skills. The installed instructions therefore tell it to follow the same workflow explicitly and ask for a reliable PDF extraction capability when native PDF retrieval is weak.

## Manual Install

Copy:

```text
install/github-copilot/copilot-instructions.md
```

to:

```text
.github/copilot-instructions.md
```

If your target project already has `.github/copilot-instructions.md`, merge the EmbeddedDocHelper section instead of overwriting the file.
