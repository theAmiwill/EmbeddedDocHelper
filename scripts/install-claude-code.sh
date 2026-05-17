#!/usr/bin/env sh
set -eu

SOURCE_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
DESTINATION="${CLAUDE_SKILLS_DIR:-"$HOME/.claude/skills"}"

mkdir -p "$DESTINATION"
cp -R "$SOURCE_ROOT/skills/vehicle-embedded-doc-indexer" "$DESTINATION/"
cp -R "$SOURCE_ROOT/skills/vehicle-embedded-doc-curator" "$DESTINATION/"

echo "Installed EmbeddedDocHelper skills -> $DESTINATION"
