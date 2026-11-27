#!/usr/bin/env bash
# set-onboarding.sh — persist value-first onboarding state.
#
# Usage:
#   bash set-onboarding.sh stage value_menu
#   bash set-onboarding.sh goal growth sub competitor input "mike tyson" stage first_sample
#
# Keys: goal | sub | input | stage
# Writes: state.json (tiktok_onboarding_<key>)
# Stdout: {"ok":true}
set -u
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
. "$SCRIPT_DIR/lib.sh"

if [ "$#" -eq 0 ] || [ $(( $# % 2 )) -ne 0 ]; then
  echo '{"ok":false,"error":"usage: set-onboarding.sh key value [key value ...]"}'
  exit 1
fi

while [ "$#" -gt 0 ]; do
  key="$1"
  value="$2"
  shift 2

  case "$key" in
    goal|input)
      state_set "tiktok_onboarding_$key" "$value"
      ;;
    sub)
      state_set "tiktok_onboarding_sub" "$value"
      ;;
    stage)
      case "$value" in
        value_menu|mini_plan|one_input|setup|first_sample|delivered|done)
          state_set "tiktok_onboarding_stage" "$value"
          ;;
        *)
          echo '{"ok":false,"error":"unsupported stage"}'
          exit 1
          ;;
      esac
      ;;
    *)
      echo '{"ok":false,"error":"unsupported key"}'
      exit 1
      ;;
  esac
done

printf '{"ok":true}\n'
