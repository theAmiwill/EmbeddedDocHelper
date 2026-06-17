#!/usr/bin/env sh
set -eu

SOURCE_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
DESTINATION="${KILO_SKILLS_DIR:-"$HOME/.kilo/skills"}"

mkdir -p "$DESTINATION"
cp -R "$SOURCE_ROOT/skills/vehicle-embedded-doc-indexer" "$DESTINATION/"
cp -R "$SOURCE_ROOT/skills/vehicle-embedded-doc-curator" "$DESTINATION/"

echo "Installed EmbeddedDocHelper skills -> $DESTINATION"

if [ "$#" -gt 0 ]; then
  "$SOURCE_ROOT/scripts/install-project-rules.sh" kilo-code "$1"
fi
