#!/usr/bin/env bash
# run-scrape.sh — run one scrape end-to-end and download the CSV.
#
# Usage:  bash run-scrape.sh <pagePath> <param> <value> [count] [key=value ...]
#   bash run-scrape.sh /tiktok-search-video query "mike tyson" 20
#   bash run-scrape.sh /tiktok-tag query beauty 30
#   bash run-scrape.sh /tiktok-profile usernames "mike,jenifer,tiktok" 3
#   bash run-scrape.sh /x-tweet-comments values "url1,url2" 200 comment_sort=recent
#   bash run-scrape.sh /x-home-timeline - "" 50 feed=following
#
# Reads:  state.json (browser_pref) — which browser the user chose during installation
# Writes: state.json (last_task_id, last_scrape_url)
# Stdout: {"status":"ready","taskId":"...","file":"...csv","rowCount":20,"empty":false,"url":"..."}
# Exit:   0 = CSV downloaded, 1 = failed (stdout has status + error)
#
# Fire-and-forget: opens the browser, verifies the process started, polls until ready,
# downloads. Never asks the user anything.
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
. "$SCRIPT_DIR/lib.sh"

if [ $# -lt 3 ]; then
  echo '{"status":"failed","error":"usage: run-scrape.sh <pagePath> <param> <value> [count] [key=value ...]"}'
  exit 2
fi

PAGEPATH="$1"
PARAM="$2"
VALUE="$3"
COUNT="${4:-}"
if [ $# -ge 4 ]; then
  shift 4
else
  shift $#
fi

# Extra options: key=value pairs (e.g. sort=latest, comment_sort=recent, pages=2)
EXTRA_QS=""
for kv in "$@"; do
  case "$kv" in
    *=*)
      k="${kv%%=*}"
      v="${kv#*=}"
      [ -n "$k" ] && EXTRA_QS="${EXTRA_QS}&${k}=$(urlencode "$v")"
      ;;
    *)
      echo '{"status":"failed","error":"extra options must be key=value"}'
      exit 2
      ;;
  esac
done

# 本地 E2E：human=1 让页面只准备 agent shim + 填表，不自动点击；
# 由外部 CDP/Playwright 派发可信点击（isTrusted=true）。默认关闭。
if [ "${MONSTERGET_HUMAN_CLICK:-0}" = "1" ]; then
  EXTRA_QS="${EXTRA_QS}&human=1"
fi

detect_browser
if [ "$BROWSER" = "none" ]; then
  echo '{"status":"failed","error":"no browser preference saved — run choose-browser.sh first"}'
  exit 1
fi

TASK_ID="$(generate_task_id)"
if [ -z "$TASK_ID" ]; then
  echo '{"status":"failed","error":"platform unreachable"}'
  exit 1
fi
state_set last_task_id "$TASK_ID"

COUNT_ARG=""
[ -n "$COUNT" ] && [ "$COUNT" != "-" ] && COUNT_ARG="&count=$COUNT"

VALUE_ARG=""
if [ -n "$PARAM" ] && [ "$PARAM" != "-" ] && [ -n "$VALUE" ]; then
  VALUE_ARG="&${PARAM}=$(urlencode "$VALUE")"
fi

URL="$SITE_URL${PAGEPATH}?auto=1&agentTaskId=${TASK_ID}${VALUE_ARG}${COUNT_ARG}${EXTRA_QS}"
state_set last_scrape_url "$URL"

# ---- open + verify the browser process actually started (never ask the user) ----
open_url "$URL"
STARTED=false
for _ in 1 2 3; do
  if browser_running; then STARTED=true; break; fi
  sleep 1
done
if [ "$STARTED" != true ]; then
  # the launch can fail silently (exe not in PATH) — retry via the full path
  open_url "$URL"
  sleep 2
  browser_running && STARTED=true
fi
if [ "$STARTED" != true ]; then
  printf '{"status":"failed","taskId":"%s","url":"%s","error":"browser did not start — open the URL manually in the extension browser"}\n' \
    "$TASK_ID" "$URL"
  exit 1
fi

# ---- poll until ready (default 20 min, batch can set MONSTERGET_POLL_TIMEOUT=1800) ----
# `not_found` (task not created YET) is NOT terminal — the page may be waiting for
# a concurrency slot (429 backoff, up to ~5 min) before it POSTs the task.
STATUS="{}"
MAX_POLLS=$(( POLL_TIMEOUT_SEC / POLL_INTERVAL ))
[ "$MAX_POLLS" -lt 1 ] && MAX_POLLS=1
for _ in $(seq 1 "$MAX_POLLS"); do
  STATUS="$(curl -s --max-time 10 "$BASE_URL/api/agent/delivery/task/$TASK_ID/status" 2>/dev/null)"
  case "$STATUS" in
    *'"status":"ready"'*)      break ;;
    *'"status":"downloaded"'*) break ;;
  esac
  sleep "$POLL_INTERVAL"
done

FILENAME="$(echo "$STATUS" | sed -n 's/.*"filename":"\([^"]*\)".*/\1/p')"
ROWCOUNT="$(echo "$STATUS" | sed -n 's/.*"resultCount":\([0-9]*\).*/\1/p')"
STATUSVAL="$(echo "$STATUS" | sed -n 's/.*"status":"\([^"]*\)".*/\1/p')"

case "$STATUSVAL" in
  ready)
    DL_DIR="$(resolve_download_dir)"
    if ! mkdir -p "$DL_DIR" 2>/dev/null; then
      printf '{"status":"failed","taskId":"%s","url":"%s","error":"cannot create download dir: %s"}\n' \
        "$TASK_ID" "$URL" "$DL_DIR"
      exit 1
    fi
    if OUT="$(download_delivery "$TASK_ID" "$DL_DIR" "$FILENAME")"; then
      EMPTY=false
      [ "${ROWCOUNT:-0}" = "0" ] && EMPTY=true
      printf '{"status":"ready","taskId":"%s","file":"%s","dir":"%s","rowCount":%s,"empty":%s,"url":"%s"}\n' \
        "$TASK_ID" "$(basename "$OUT")" "$DL_DIR" "${ROWCOUNT:-0}" "$EMPTY" "$URL"
    else
      rc=$?
      case "$rc" in
        3) ERR="downloaded file is empty" ;;
        4) ERR="data buffer unavailable after retries — run again (new taskId)" ;;
        5) ERR="CSV is tombstoned (one download only) — generate a new taskId and scrape again" ;;
        *) ERR="download failed — check platform reachability" ;;
      esac
      if [ "$rc" = "5" ]; then
        printf '{"status":"already_downloaded","taskId":"%s","error":"%s"}\n' "$TASK_ID" "$ERR"
      else
        printf '{"status":"failed","taskId":"%s","url":"%s","error":"%s"}\n' "$TASK_ID" "$URL" "$ERR"
      fi
      exit 1
    fi
    ;;
  downloaded)
    printf '{"status":"already_downloaded","taskId":"%s","error":"CSV is tombstoned (one download only) — generate a new taskId and scrape again"}\n' \
      "$TASK_ID"
    exit 1
    ;;
  *)
    if echo "$STATUS" | grep -q 'not_found'; then
      printf '{"status":"not_found","taskId":"%s","url":"%s","error":"task was never created — the page did not load, the extension is not ready, or the platform is still queued"}\n' \
        "$TASK_ID" "$URL"
    else
      printf '{"status":"timeout","taskId":"%s","url":"%s","error":"not ready within %s seconds — extension missing, not logged in, or the tab was closed"}\n' \
        "$TASK_ID" "$URL" "$POLL_TIMEOUT_SEC"
    fi
    exit 1
    ;;
esac
