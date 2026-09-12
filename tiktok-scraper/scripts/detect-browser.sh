#!/usr/bin/env bash
# detect-browser.sh — detect which browser has the MonsterGet extension installed.
#
# Usage:  bash detect-browser.sh
# Reads:  state.json (browser hint, informational only — detection is always re-run)
# Writes: state.json (os, browser, browser_exe, browser_fullpath, extension)
# Stdout: {"os":"windows","browser":"edge","browser_exe":"msedge","extension":true}
# Exit:   0 = extension found, 1 = not found (stdout still valid JSON)
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
. "$SCRIPT_DIR/lib.sh"

detect_browser
EXT=false
[ "$BROWSER" != "none" ] && EXT=true

state_set os "$(detect_os)"
state_set browser "$BROWSER"
state_set browser_exe "$BROWSER_EXE"
state_set browser_fullpath "$BROWSER_FULLPATH"
state_set extension "$EXT"

printf '{"os":"%s","browser":"%s","browser_exe":"%s","extension":%s}\n' \
  "$(detect_os)" "$BROWSER" "$BROWSER_EXE" "$EXT"

[ "$EXT" = true ]
