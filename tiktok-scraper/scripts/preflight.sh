#!/usr/bin/env bash
# preflight.sh — silent programmatic preflight (SKILL.md Step 0.6).
#
# Runs: browser/extension detection → platform reachability → MonsterGet login → TikTok login.
# No user interaction, no questions. Short login probes (3 × 5s) are enough to detect an
# already-finished setup; if they time out, escalate to the interactive Step 0 flow.
#
# Usage:  bash preflight.sh
# Writes: state.json (extension, platform_reachable, monsterget_login, tiktok_login, checked_at)
# Stdout: {"ready":true,"next":"","extension":true,"platform_reachable":true,
#          "monsterget_login":true,"tiktok_login":true,"browser":"edge","os":"windows"}
#   ready = all 3 user-facing steps pass   next = first failing step, "" when ready
#   next is one of: extension | monsterget_login | tiktok_login | platform_reachable
# Exit:   0 = all checks pass, 1 = at least one failed (stdout says which)
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
. "$SCRIPT_DIR/lib.sh"

# ① extension + browser (local file scan, ~0.1s)
bash "$SCRIPT_DIR/detect-browser.sh" >/dev/null 2>&1
EXT=false
[ "$(state_get browser)" != "none" ] && EXT=true

# ② platform reachability
HTTP="$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$BASE_URL/api/agent/generate-task-id" 2>/dev/null)"
REACH=false
[ "$HTTP" = "200" ] && REACH=true

# ③ logins — only meaningful when the extension exists and the platform answers
MG=false
TK=false
if [ "$EXT" = true ] && [ "$REACH" = true ]; then
  MONSTERGET_POLLS=3 bash "$SCRIPT_DIR/check-login.sh" monsterget >/dev/null 2>&1 && MG=true
  MONSTERGET_POLLS=3 bash "$SCRIPT_DIR/check-login.sh" tiktok    >/dev/null 2>&1 && TK=true
fi

state_set extension "$EXT"
state_set platform_reachable "$REACH"
state_set monsterget_login "$MG"
state_set tiktok_login "$TK"
state_set checked_at "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# `next` = the first step the agent must guide the user through, in ①→②→③ order.
# Empty string means all three pass and the user can scrape right away.
NEXT=""
if [ "$EXT" != true ]; then
  NEXT="extension"
elif [ "$MG" != true ]; then
  NEXT="monsterget_login"
elif [ "$TK" != true ]; then
  NEXT="tiktok_login"
elif [ "$REACH" != true ]; then
  NEXT="platform_reachable"
fi

READY=false
[ -z "$NEXT" ] && READY=true

printf '{"ready":%s,"next":"%s","extension":%s,"platform_reachable":%s,"monsterget_login":%s,"tiktok_login":%s,"browser":"%s","os":"%s"}\n' \
  "$READY" "$NEXT" "$EXT" "$REACH" "$MG" "$TK" "$(state_get browser)" "$(detect_os)"

[ -z "$NEXT" ]
