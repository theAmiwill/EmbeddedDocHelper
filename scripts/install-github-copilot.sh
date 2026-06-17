#!/usr/bin/env sh
set -eu

if [ "$#" -lt 1 ]; then
  echo "usage: $0 /path/to/target-project" >&2
  exit 2
fi

TARGET_PROJECT="$(CDPATH= cd -- "$1" && pwd)"
SOURCE_ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
GITHUB_DIR="$TARGET_PROJECT/.github"
REPO_INSTRUCTIONS="$GITHUB_DIR/copilot-instructions.md"
TEMPLATE_ROOT="$SOURCE_ROOT/install/github-copilot"
MARKER_START="<!-- EmbeddedDocHelper start -->"
MARKER_END="<!-- EmbeddedDocHelper end -->"

mkdir -p "$GITHUB_DIR"

if [ -f "$REPO_INSTRUCTIONS" ]; then
  if grep -q "$MARKER_START" "$REPO_INSTRUCTIONS"; then
    echo "EmbeddedDocHelper section already present -> $REPO_INSTRUCTIONS"
  else
    {
      printf '\n%s\n' "$MARKER_START"
      cat "$SOURCE_ROOT/install/agent-rules/embedded-doc-helper.md"
      printf '\n'
      cat "$TEMPLATE_ROOT/copilot-instructions.md"
      printf '\n%s\n' "$MARKER_END"
    } >> "$REPO_INSTRUCTIONS"
    echo "Appended EmbeddedDocHelper section -> $REPO_INSTRUCTIONS"
  fi
else
  {
    printf '%s\n' "$MARKER_START"
    cat "$SOURCE_ROOT/install/agent-rules/embedded-doc-helper.md"
    printf '\n'
    cat "$TEMPLATE_ROOT/copilot-instructions.md"
    printf '\n%s\n' "$MARKER_END"
  } > "$REPO_INSTRUCTIONS"
  echo "Created $REPO_INSTRUCTIONS"
fi
