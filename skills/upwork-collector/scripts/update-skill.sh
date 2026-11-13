#!/usr/bin/env bash
# update-skill.sh — check for + apply skill updates from GitHub.
#
# VERSION.json is the single source of truth. No need to read SKILL.md
# or API endpoints — just compare version strings.
#
# Usage:  bash update-skill.sh
# Stdout: JSON — success or failure always returns exit 0 (non-fatal)
#
# Output examples:
#   {"updated":false,"current_version":"1.1.0","extension_recommended":"2.3.0","extension_install_url":"https://...","error":null}
#   {"updated":true,"old_version":"1.0.0","new_version":"1.1.0","changelog":"v1.1.0: ...","extension_recommended":"2.3.0","extension_install_url":"https://..."}
#   {"updated":false,"error":"cannot fetch remote version — network issue"}
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

LOCAL_VERSION_FILE="$HOME/.monsterget/version.json"
REPO="monsterget-com/skills"
BRANCH="main"
REMOTE_URL="https://raw.githubusercontent.com/$REPO/$BRANCH/skills/upwork-collector/VERSION.json"

# ---- helpers ----

json_val() {
  # Extract a (non-nested) string value from a JSON key.
  # Usage:  json_val "skill" < file.json   or   echo "$json" | json_val "skill"
  sed -n 's/.*"'"$1"'"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1
}

# ver_gt A B — true（exit 0）当 A 严格大于 B；支持 1.2.3 形式。
# 用于防止「本地版本比远端新」时被 update-skill.sh 降级覆盖。
ver_gt() {
  [ "$1" = "$2" ] && return 1
  local first
  first="$(printf '%s\n%s\n' "$1" "$2" | sort -V 2>/dev/null | head -1)"
  [ "$first" = "$2" ]
}

# ---- read local version ----
# The skill's own VERSION.json is the source of truth for its version.
# ~/.monsterget/version.json is SHARED across skills (tiktok-collector's
# update-skill.sh rewrites that file wholesale), so it only carries the
# shared fields (extension_version / scrapers_api) — never a per-skill
# version, which another skill's rewrite would clobber.

LOCAL_SKILL="0"
LOCAL_EXT="unknown"
LOCAL_API="0"

if [ -f "$SKILL_DIR/VERSION.json" ]; then
  LOCAL_SKILL="$(json_val "skill" < "$SKILL_DIR/VERSION.json")"
  [ -z "$LOCAL_SKILL" ] && LOCAL_SKILL="0"
  LOCAL_API="$(json_val "scrapers_api" < "$SKILL_DIR/VERSION.json")"
  [ -z "$LOCAL_API" ] && LOCAL_API="0"
fi
if [ -f "$LOCAL_VERSION_FILE" ]; then
  # Shared fields only — informational output, not version comparison
  LOCAL_EXT="$(json_val "extension_version" < "$LOCAL_VERSION_FILE")"
  [ -z "$LOCAL_EXT" ] && LOCAL_EXT="unknown"
  API_FROM_SHARED="$(json_val "scrapers_api" < "$LOCAL_VERSION_FILE")"
  [ -z "$API_FROM_SHARED" ] || LOCAL_API="$API_FROM_SHARED"
fi

# ---- fetch remote version ----

REMOTE_JSON="$(curl -sL --max-time 15 "$REMOTE_URL" 2>/dev/null)" || REMOTE_JSON=""
if [ -z "$REMOTE_JSON" ]; then
  printf '{"updated":false,"current_version":"%s","scrapers_api":"%s","extension_recommended":"%s","extension_install_url":"","error":"cannot fetch remote version — network issue"}\n' \
    "$LOCAL_SKILL" "$LOCAL_API" "$LOCAL_EXT"
  exit 0
fi

REMOTE_SKILL="$(printf '%s' "$REMOTE_JSON" | json_val "skill")"
[ -z "$REMOTE_SKILL" ] && REMOTE_SKILL="0"
REMOTE_EXT="$(printf '%s' "$REMOTE_JSON" | json_val "extension_recommended")"
[ -z "$REMOTE_EXT" ] && REMOTE_EXT="unknown"
REMOTE_INSTALL_URL="$(printf '%s' "$REMOTE_JSON" | json_val "extension_install_url")"
[ -z "$REMOTE_INSTALL_URL" ] && REMOTE_INSTALL_URL="https://monsterget.com/install"
REMOTE_CHANGELOG="$(printf '%s' "$REMOTE_JSON" | json_val "changelog")"
REMOTE_VER="$(printf '%s' "$REMOTE_JSON" | json_val "version")"
REMOTE_API="$(printf '%s' "$REMOTE_JSON" | json_val "scrapers_api")"
[ -z "$REMOTE_API" ] && REMOTE_API="0"

# ---- compare ----

if ! ver_gt "$REMOTE_SKILL" "$LOCAL_SKILL"; then
  # 远端版本 <= 本地版本（或远端缺失/无法解析）→ 保持本地，绝不降级
  printf '{"updated":false,"current_version":"%s","scrapers_api":"%s","extension_recommended":"%s","extension_install_url":"%s","error":null}\n' \
    "$LOCAL_SKILL" "$LOCAL_API" "$REMOTE_EXT" "$REMOTE_INSTALL_URL"
  exit 0
fi

# ---- update: download and replace ----

TMP_DIR="$(mktemp -d 2>/dev/null || echo "$HOME/.monsterget/_update_tmp")"
[ -d "$TMP_DIR" ] || mkdir -p "$TMP_DIR"
trap 'rm -rf "$TMP_DIR"' EXIT

UPDATED=false
if curl -sL --max-time 120 \
  "https://codeload.github.com/$REPO/tar.gz/refs/heads/$BRANCH" \
  -o "$TMP_DIR/repo.tar.gz" &&
  tar -xzf "$TMP_DIR/repo.tar.gz" -C "$TMP_DIR" 2>/dev/null; then

  SRC="$TMP_DIR/skills-$BRANCH/skills/upwork-collector"
  if [ -f "$SRC/VERSION.json" ]; then
    # Verify the staged files look valid before overwriting
    STAGED_SKILL="$(json_val "skill" < "$SRC/VERSION.json")"
    if [ -n "$STAGED_SKILL" ]; then
      # Remove old scripts, copy entire tree (SKILL.md + scripts + VERSION.json + AGENTS.md + INSTALL.md)
      rm -rf "$SKILL_DIR/scripts"
      cp -r "$SRC/." "$SKILL_DIR/"
      chmod +x "$SKILL_DIR/scripts/"*.sh 2>/dev/null || true
      UPDATED=true
    fi
  fi
fi

# ---- persist local version record ----
# Shared file: update ONLY the shared fields in place (awk in-place update).
# Never rewrite the whole file — tiktok-collector's update-skill.sh owns the
# full file and its `skill_version` field; clobbering it here would corrupt
# the other skill's state. This skill's own version stays in its VERSION.json.

mkdir -p "$HOME/.monsterget"
if [ ! -f "$LOCAL_VERSION_FILE" ]; then
  # Bootstrap the shared file only if it does not exist yet
  printf '{\n  "skill_version": "0",\n  "extension_version": "unknown",\n  "scrapers_api": "%s"\n}\n' "$REMOTE_API" > "$LOCAL_VERSION_FILE"
else
  # Portable in-place update of just the scrapers_api field (no jq dependency)
  awk -v v="$REMOTE_API" '{ if ($0 ~ /"scrapers_api":/) sub(/"scrapers_api":[[:space:]]*"[^"]*"/, "\"scrapers_api\": \"" v "\""); print }' \
    "$LOCAL_VERSION_FILE" > "$LOCAL_VERSION_FILE.tmp" && mv "$LOCAL_VERSION_FILE.tmp" "$LOCAL_VERSION_FILE"
fi

# ---- output ----

if [ "$UPDATED" = true ]; then
  printf '{"updated":true,"old_version":"%s","new_version":"%s","changelog":"%s","scrapers_api":"%s","extension_recommended":"%s","extension_install_url":"%s"}\n' \
    "$LOCAL_SKILL" "$REMOTE_SKILL" "$REMOTE_CHANGELOG" "$REMOTE_API" "$REMOTE_EXT" "$REMOTE_INSTALL_URL"
else
  printf '{"updated":false,"current_version":"%s","scrapers_api":"%s","extension_recommended":"%s","extension_install_url":"%s","error":"download failed — skill not updated; network may be unavailable"}\n' \
    "$LOCAL_SKILL" "$LOCAL_API" "$LOCAL_EXT" "$REMOTE_INSTALL_URL"
fi
exit 0