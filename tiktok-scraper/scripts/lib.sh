#!/usr/bin/env bash
# lib.sh — shared helpers for MonsterGet skill scripts.
# Source this file from other scripts; it only defines functions/variables, runs nothing.
#
# Configuration via environment (all optional):
#   MONSTERGET_BASE_URL   API host           (default https://monsterget.com)
#   MONSTERGET_SITE_URL   page host          (default = BASE_URL)
#   MONSTERGET_STATE_DIR  state directory    (default ~/.monsterget)
#   MONSTERGET_STATE_FILE state file         (default $STATE_DIR/state.json)
#   MONSTERGET_POLLS      login-check polls  (default 12 × 5s)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
STATE_DIR="${MONSTERGET_STATE_DIR:-$HOME/.monsterget}"
STATE_FILE="${MONSTERGET_STATE_FILE:-$STATE_DIR/state.json}"
BASE_URL="${MONSTERGET_BASE_URL:-https://monsterget.com}"
SITE_URL="${MONSTERGET_SITE_URL:-$BASE_URL}"
POLLS="${MONSTERGET_POLLS:-12}"

# ---------------------------------------------------------------------------
# OS detection — windows | macos | linux | unknown
# ---------------------------------------------------------------------------
detect_os() {
  case "$(uname -s 2>/dev/null)" in
    MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
    Darwin*)              echo "macos"   ;;
    Linux*)               echo "linux"   ;;
    *)                    echo "unknown" ;;
  esac
}

# ---------------------------------------------------------------------------
# State persistence — tiny JSON key/value store (string values only)
# ---------------------------------------------------------------------------
state_init() {
  mkdir -p "$STATE_DIR" 2>/dev/null
  [ -f "$STATE_FILE" ] || printf '{}' > "$STATE_FILE"
}

# state_get <key>  → prints the value (or nothing if missing)
state_get() {
  state_init
  grep -o "\"$1\":\"[^\"]*\"" "$STATE_FILE" 2>/dev/null | head -n1 | sed "s/\"$1\":\"//; s/\"$//"
}

# state_set <key> <value>  → upsert a string value, keeps other keys intact.
# The state file is single-line JSON, so grep -v (line-based) would delete the whole
# line when the key exists — use awk for a true in-place key replacement instead.
state_set() {
  local key="$1" value="${2//\"/\\\"}"
  state_init
  awk -v k="$key" -v v="$value" '
    BEGIN { gsub(/&/, "\\&", v); gsub(/\\/, "\\\\", v) }
    {
      if ($0 ~ "\"" k "\":") {
        sub("\"" k "\":\"[^\"]*\"", "\"" k "\":\"" v "\"")
      } else if ($0 ~ /^\{[[:space:]]*\}$/) {
        $0 = "{\"" k "\":\"" v "\"}"
      } else {
        sub(/\}[[:space:]]*$/, ",\"" k "\":\"" v "\"}")
      }
      print
    }' "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"
}

# ---------------------------------------------------------------------------
# Browser detection — which browser has the MonsterGet extension installed.
# Sets globals: BROWSER, BROWSER_EXE, BROWSER_FULLPATH
#   BROWSER=edge|chrome|none
# ---------------------------------------------------------------------------
BROWSER="none"; BROWSER_EXE=""; BROWSER_FULLPATH=""

_try_browser() {
  local name="$1" pref="$2" full="$3" exe="$4"
  if [ -f "$pref" ] && grep -q "MonsterGet" "$pref" 2>/dev/null; then
    BROWSER="$name"; BROWSER_EXE="$exe"; BROWSER_FULLPATH="$full"; return 0
  fi
  return 1
}

detect_browser() {
  BROWSER="none"; BROWSER_EXE=""; BROWSER_FULLPATH=""
  case "$(detect_os)" in
    windows)
      _try_browser edge   "$HOME/AppData/Local/Microsoft/Edge/User Data/Default/Preferences" "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" msedge ||
      _try_browser chrome "$HOME/AppData/Local/Google/Chrome/User Data/Default/Preferences" "/c/Program Files/Google/Chrome/Application/chrome.exe" chrome
      ;;
    macos)
      _try_browser edge   "$HOME/Library/Application Support/Microsoft Edge/Default/Preferences" "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" "Microsoft Edge" ||
      _try_browser chrome "$HOME/Library/Application Support/Google/Chrome/Default/Preferences" "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" "Google Chrome"
      ;;
    linux)
      _try_browser edge   "$HOME/.config/microsoft-edge/Default/Preferences" "" "microsoft-edge" ||
      _try_browser chrome "$HOME/.config/google-chrome/Default/Preferences" "" "google-chrome"
      ;;
    *) : ;;
  esac
}

# ---------------------------------------------------------------------------
# Browser launch & process verification
# ---------------------------------------------------------------------------
# open_url <url> — fire-and-forget; exit 0 if a launch attempt succeeded
open_url() {
  local url="$1"
  case "$(detect_os)" in
    windows)
      if command -v cmd >/dev/null 2>&1; then
        MSYS_NO_PATHCONV=1 cmd /c start "" "$url" >/dev/null 2>&1 && return 0
      fi
      [ -n "$BROWSER_FULLPATH" ] && [ -f "$BROWSER_FULLPATH" ] && "$BROWSER_FULLPATH" "$url" >/dev/null 2>&1 && return 0
      [ -n "$BROWSER_EXE" ] && command -v "$BROWSER_EXE" >/dev/null 2>&1 && "$BROWSER_EXE" "$url" >/dev/null 2>&1 && return 0
      return 1
      ;;
    macos)
      [ -n "$BROWSER_FULLPATH" ] && [ -f "$BROWSER_FULLPATH" ] && "$BROWSER_FULLPATH" "$url" >/dev/null 2>&1 && return 0
      open "$url" >/dev/null 2>&1 && return 0
      return 1
      ;;
    linux)
      [ -n "$BROWSER_EXE" ] && command -v "$BROWSER_EXE" >/dev/null 2>&1 && "$BROWSER_EXE" "$url" >/dev/null 2>&1 && return 0
      command -v xdg-open >/dev/null 2>&1 && xdg-open "$url" >/dev/null 2>&1 && return 0
      return 1
      ;;
    *) return 1 ;;
  esac
}

# browser_running — exit 0 if the extension browser's process is alive
browser_running() {
  local exe="$BROWSER_EXE"
  [ -z "$exe" ] && return 1
  case "$(detect_os)" in
    windows)
      MSYS_NO_PATHCONV=1 tasklist /fi "IMAGENAME eq $exe.exe" 2>/dev/null | grep -qi "$exe"
      ;;
    macos|linux)
      pgrep -x "$exe" >/dev/null 2>&1 || pgrep -f "$exe" >/dev/null 2>&1
      ;;
    *) return 1 ;;
  esac
}

# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------
generate_task_id() {
  curl -s --max-time 10 "$BASE_URL/api/agent/generate-task-id" 2>/dev/null | sed -n 's/.*"taskId":"\([^"]*\)".*/\1/p'
}

# urlencode <string> — RFC 3986 percent-encoding, byte-safe for UTF-8
urlencode() {
  local LC_ALL=C
  local s="$1" c out="" i hex=""
  for ((i=0; i<${#s}; i++)); do
    c="${s:i:1}"
    case "$c" in
      [a-zA-Z0-9._~-]) out+="$c" ;;
      "'")             out+="%27" ;;
      *)               printf -v hex '%%%02X' "'$c"; out+="$hex" ;;
    esac
  done
  printf '%s' "$out"
}
