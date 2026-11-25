#!/usr/bin/env bash
# resolve-runtime.sh — find a collector's run-scrape.sh across install layouts.
#
# Usage: resolve-runtime.sh <collector-skill>
#   resolve-runtime.sh tiktok-collector
#
# Prints the absolute path of run-scrape.sh, or exits 1 with a clear error.
set -u

SKILL="${1:-}"
if [ -z "$SKILL" ]; then
  echo "usage: resolve-runtime.sh <collector-skill>" >&2
  exit 2
fi

for root in \
  "${MONSTERGET_HOME:-$HOME/.monsterget}/skills" \
  ".agents/skills" \
  "$HOME/.agents/skills" \
  ".claude/skills" \
  "$HOME/.claude/skills" \
  ".codex/skills" \
  "$HOME/.codex/skills" \
  ".cursor/skills" \
  "$HOME/.cursor/skills" \
  ".windsurf/skills" \
  "$HOME/.windsurf/skills" \
  ".opencode/skills" \
  "$HOME/.opencode/skills"
do
  f="$root/$SKILL/scripts/run-scrape.sh"
  if [ -f "$f" ]; then
    printf '%s\n' "$f"
    exit 0
  fi
done

cat >&2 <<EOF
collector_not_found: $SKILL
Install it first:
  - Say: "Install $SKILL from https://github.com/monsterget-com/skills"
  - Or:  npx skills add monsterget-com/skills --skill $SKILL
EOF
exit 1
