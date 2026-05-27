# Install for Codex

## Global Install

Copy both skill directories into your Codex skills directory:

```powershell
.\scripts\install-codex.ps1
```

macOS/Linux:

```sh
./scripts/install-codex.sh
```

Equivalent manual install:

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex\skills"
Copy-Item -Recurse -Force ".\skills\vehicle-embedded-doc-indexer" "$HOME\.codex\skills\"
Copy-Item -Recurse -Force ".\skills\vehicle-embedded-doc-curator" "$HOME\.codex\skills\"
```

macOS/Linux manual install:

```sh
mkdir -p ~/.codex/skills
cp -R ./skills/vehicle-embedded-doc-indexer ~/.codex/skills/
cp -R ./skills/vehicle-embedded-doc-curator ~/.codex/skills/
```

Restart Codex if the skills do not appear immediately.

## Suggested Use

In a project with hardware documents, software manuals, and optionally explicit demo/current code paths:

```text
Use $vehicle-embedded-doc-indexer to create layered .vehicle-embedded-docs/ memory. Reuse any copied portable hardware/software packages before scanning source documents.
```

Later, in a new conversation:

```text
Use $vehicle-embedded-doc-curator to answer from .vehicle-embedded-docs/, keeping portable knowledge separate from project code context.
```
