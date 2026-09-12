#!/usr/bin/env bash
# choose-browser.sh — save the user's browser choice when several have the extension.
#
# Usage:  bash choose-browser.sh edge|chrome
# Reads:  state.json (none needed beyond detection)
# Writes: state.json (browser_pref = the chosen browser)
# Stdout: {"ok":true,"browser":"edge","browser_exe":"msedge","browsers":["edge","chrome"]}
# Exit:   0 = choice saved, 1 = refused (that browser has no extension)
#
# Call this ONLY after asking the user which browser to use, and only when
# detect-browser.sh reported `need_choice:true`. The choice is persisted, so the
# question is asked at most once — later sessions reuse it automatically.
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
. "$SCRIPT_DIR/lib.sh"

WANT="${1:-}"
case "$WANT" in
  edge|chrome) : ;;
  *) echo '{"ok":false,"error":"usage: choose-browser.sh edge|chrome"}'; exit 1 ;;
esac

detect_browser
if [ "$BROWSER" = "none" ]; then
  echo '{"ok":false,"error":"no browser has the MonsterGet extension — install it first"}'
  exit 1
fi

case " $BROWSERS " in
  *" $WANT "*) : ;;
  *)
    printf '{"ok":false,"error":"%s does not have the MonsterGet extension","browsers":%s}\n' \
      "$WANT" "$(browser_choices_json)"
    exit 1
    ;;
esac

state_set browser_pref "$WANT"
detect_browser   # re-resolve so the reported browser/exe reflect the new choice

printf '{"ok":true,"browser":"%s","browser_exe":"%s","browsers":%s,"chosen_by":"%s"}\n' \
  "$BROWSER" "$BROWSER_EXE" "$(browser_choices_json)" "$CHOSEN_BY"
