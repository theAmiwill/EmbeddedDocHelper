# Install for Claude Code

Claude Code supports skills as directories containing `SKILL.md`.

## Global Install

```powershell
.\scripts\install-claude-code.ps1
```

macOS/Linux:

```sh
./scripts/install-claude-code.sh
```

Equivalent manual install:

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude\skills"
Copy-Item -Recurse -Force ".\skills\vehicle-embedded-doc-indexer" "$HOME\.claude\skills\"
Copy-Item -Recurse -Force ".\skills\vehicle-embedded-doc-curator" "$HOME\.claude\skills\"
```

macOS/Linux manual install:

```sh
mkdir -p ~/.claude/skills
cp -R ./skills/vehicle-embedded-doc-indexer ~/.claude/skills/
cp -R ./skills/vehicle-embedded-doc-curator ~/.claude/skills/
```

Claude Code personal skills live under `~/.claude/skills/<skill-name>/SKILL.md`. Project skills can also live under `.claude/skills/<skill-name>/SKILL.md`.

Because these skills depend heavily on PDF retrieval, also install Anthropic's official `skills/pdf` when your Claude Code environment supports it.

## Project Rules

To also append EmbeddedDocHelper constraints to a project's `CLAUDE.md`:

```powershell
.\scripts\install-claude-code.ps1 -TargetProject C:\path\to\your\project
```

macOS/Linux:

```sh
./scripts/install-claude-code.sh /path/to/your/project
```

These rules help Claude Code follow the installed skill workflows even when automatic skill invocation is weak.

## Suggested Use

```text
/vehicle-embedded-doc-indexer
```

or ask naturally:

```text
Index this embedded project with portable hardware/software documents and the explicit code directories I provide.
```

Then reuse the generated `.vehicle-embedded-docs/` directory. `portable/` can be copied to a new project using the same chip/software stack; `project/` should stay project-specific.

```text
/vehicle-embedded-doc-curator
```
