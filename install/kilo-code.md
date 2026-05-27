# Install for Kilo Code

Kilo Code supports Agent Skills as folders containing `SKILL.md`.

## Global Install

```powershell
.\scripts\install-kilo-code.ps1
```

macOS/Linux:

```sh
./scripts/install-kilo-code.sh
```

Equivalent manual install:

```powershell
New-Item -ItemType Directory -Force "$HOME\.kilo\skills"
Copy-Item -Recurse -Force ".\skills\vehicle-embedded-doc-indexer" "$HOME\.kilo\skills\"
Copy-Item -Recurse -Force ".\skills\vehicle-embedded-doc-curator" "$HOME\.kilo\skills\"
```

macOS/Linux manual install:

```sh
mkdir -p ~/.kilo/skills
cp -R ./skills/vehicle-embedded-doc-indexer ~/.kilo/skills/
cp -R ./skills/vehicle-embedded-doc-curator ~/.kilo/skills/
```

Kilo Code also supports project skills under `.kilo/skills/`.

## Suggested Use

Ask Kilo Code to use the indexer first:

```text
Use vehicle-embedded-doc-indexer to create layered .vehicle-embedded-docs/ for this project, reusing copied portable hardware/software packages when available.
```

Then ask targeted questions with the curator:

```text
Use vehicle-embedded-doc-curator to locate the CAN0 hardware path, map it to software guide sections, and use code only as project context.
```
