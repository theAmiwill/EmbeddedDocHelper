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

## Suggested Use

```text
/vehicle-embedded-doc-indexer
```

or ask naturally:

```text
Index the schematics, chip manual, and Excel attachments for this embedded project.
```

Then reuse the generated `.vehicle-embedded-docs/` directory:

```text
/vehicle-embedded-doc-curator
```
