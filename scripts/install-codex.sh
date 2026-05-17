#!/usr/bin/env sh
set -eu

SOURCE_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
DESTINATION="${CODEX_SKILLS_DIR:-"$HOME/.codex/skills"}"

mkdir -p "$DESTINATION"
cp -R "$SOURCE_ROOT/skills/vehicle-embedded-doc-indexer" "$DESTINATION/"
cp -R "$SOURCE_ROOT/skills/vehicle-embedded-doc-curator" "$DESTINATION/"

echo "Installed EmbeddedDocHelper skills -> $DESTINATION"
