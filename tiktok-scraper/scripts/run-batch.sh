#!/usr/bin/env bash
# run-batch.sh — run several scrapes serially, with a random pause between them.
#
# Usage:  bash run-batch.sh "<spec>" ["<spec>" ...]
#   bash run-batch.sh "/tiktok-search-video query mike tyson 20" "/tiktok-tag query kpop 30"
#   bash run-batch.sh "/tiktok-profile usernames mike,jenifer,tiktok 3"
#
# Each spec is ONE quoted string: <pagePath> <param> <value> [count].
# Between consecutive scrapes it sleeps a random 15-45s (env overrides:
#   MONSTERGET_DELAY_MIN / MONSTERGET_DELAY_MAX), so a batch does not look like
# a machine opening window after window. There is NO delay after the last one.
#
# Stdout: one JSON object listing every result:
#   {"total":3,"ok":2,"failed":1,
#    "results":[{"status":"ready",...}, {"status":"failed",...}]}
# Exit:   0 = all scrapes OK, 1 = at least one failed
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
. "$SCRIPT_DIR/lib.sh"

DELAY_MIN="${MONSTERGET_DELAY_MIN:-15}"
DELAY_MAX="${MONSTERGET_DELAY_MAX:-45}"

if [ $# -lt 1 ]; then
  echo '{"status":"failed","error":"usage: run-batch.sh <spec> [spec ...]"}'
  exit 2
fi

TOTAL=0; OK=0; FAILED=0
RESULTS=""
FIRST=1
for spec in "$@"; do
  # random pause BETWEEN scrapes, never after the last
  if [ "$FIRST" -ne 1 ]; then
    random_delay "$DELAY_MIN" "$DELAY_MAX"
    printf '[batch] pause %ss before next scrape\n' "$RAND_DELAY" >&2
  fi
  FIRST=0
  TOTAL=$((TOTAL + 1))

  # shellcheck disable=SC2086  # the spec is intentionally word-split
  OUT="$(bash "$SCRIPT_DIR/run-scrape.sh" $spec 2>/dev/null)"
  RC=$?

  if [ "$RC" -eq 0 ]; then
    OK=$((OK + 1))
  else
    FAILED=$((FAILED + 1))
  fi
  [ -n "$RESULTS" ] && RESULTS="$RESULTS,"
  RESULTS="$RESULTS$OUT"
done

printf '{"total":%s,"ok":%s,"failed":%s,"results":[%s]}\n' "$TOTAL" "$OK" "$FAILED" "$RESULTS"
[ "$FAILED" -eq 0 ]
