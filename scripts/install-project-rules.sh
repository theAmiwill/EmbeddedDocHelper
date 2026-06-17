#!/usr/bin/env sh
set -eu

if [ "$#" -lt 2 ]; then
  echo "usage: $0 codex|claude-code|kilo-code /path/to/target-project" >&2
  exit 2
fi

AGENT="$1"
TARGET_PROJECT="$(CDPATH= cd -- "$2" && pwd)"
SOURCE_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
RULE_ROOT="$SOURCE_ROOT/install/agent-rules"
RULE_FILE="$RULE_ROOT/embedded-doc-helper.md"
MARKER_START="<!-- EmbeddedDocHelper start -->"
MARKER_END="<!-- EmbeddedDocHelper end -->"

case "$AGENT" in
  codex) TARGET_FILE="$TARGET_PROJECT/AGENTS.md" ;;
  claude-code) TARGET_FILE="$TARGET_PROJECT/CLAUDE.md" ;;
  kilo-code) TARGET_FILE="$TARGET_PROJECT/.kilocode/rules/embedded-doc-helper.md" ;;
  *)
    echo "unsupported agent: $AGENT" >&2
    exit 2
    ;;
esac

if [ ! -f "$RULE_FILE" ]; then
  echo "missing rules template: $RULE_FILE" >&2
  exit 1
fi

mkdir -p "$(dirname -- "$TARGET_FILE")"

if [ -f "$TARGET_FILE" ] && grep -q "$MARKER_START" "$TARGET_FILE"; then
  echo "EmbeddedDocHelper section already present -> $TARGET_FILE"
  exit 0
fi

{
  if [ -f "$TARGET_FILE" ]; then
    printf '\n'
  fi
  printf '%s\n' "$MARKER_START"
  cat "$RULE_FILE"
  printf '\n%s\n' "$MARKER_END"
} >> "$TARGET_FILE"

echo "Installed EmbeddedDocHelper rules -> $TARGET_FILE"
