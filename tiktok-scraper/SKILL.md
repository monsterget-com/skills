---
name: tiktok-scraper
description: 🎁 Permanently free — 10M entries on signup, 1 concurrent window. Zero-install skill: open a browser URL, the extension + logged-in session do the rest. TikTok video search, creator discovery, hashtag collection, user video export to CSV. Works with Claude Code, Codex, Cursor, Windsurf, ChatGPT (any AI client). No Python packages, no credentials, no headless setup.
---

# TikTok Scraper

> 🎁 **Permanently free · 10 million entries on signup · 1 concurrent window for free users**
> *(Members unlock more parallel windows.)*

## What is this?

A skill that lets **any AI assistant** (Claude Code, Codex, Cursor, Windsurf, ChatGPT…) scrape TikTok data — video search, creator discovery, hashtag collection, or a specific creator's videos — and return it as a CSV. You don't install Python packages, configure headless browsers, or manage credentials. The AI orchestrates: it generates a task ID, opens a URL in the **user's own browser**, and downloads the result.

**Why a browser + extension?** The actual scrape runs inside the user's real TikTok session (logged in, with the [MonsterGet](https://monsterget.com) browser extension installed). That's what keeps the accounts anti-ban safe. There is no server-side TikTok scraping — the data is collected right where the user is already logged in.

**First-time setup (one-time, ~2 minutes):** the user registers a free account at [monsterget.com](https://monsterget.com) and installs the extension (Chrome/Edge). Everything after that is repeatable and instant.

Scrape TikTok data through the MonsterGet platform running on the user's machine — **zero install, zero credentials, zero Python packages for the user**. The scrape runs in the **user's real browser** with an installed extension and logged-in session (anti-ban core). The AI just orchestrates.

## When to use

User wants TikTok data: video search, user/creator search, hashtag/tag search, or a specific creator's videos — typically for market research, competitor analysis, influencer discovery, content monitoring.

## 🌍 Language rule (read before anything else)

**Always communicate with the user in the user's own language.** Every message you print for the user — the setup guidance, progress updates, failure explanations, the final result summary — must be in the language the user writes to you in. This skill's instructions are written in English for precision, but that is *not* the language you speak to the user.

- User writes Chinese → reply in Chinese
- User writes Japanese → reply in Japanese
- User writes Spanish / Portuguese / Korean / … → reply in that language
- Never mix two languages in one user-facing message

The zh-CN localized wording for the setup guidance is provided verbatim in the **Appendix** at the end of this file. Use it only when the user's language is Chinese; otherwise translate the English version yourself.

## Architecture (what actually happens)

```
AI ──1. GET {SITE_URL}/api/agent/generate-task-id ──▶ {"taskId":"<uuid>"}
AI ──2. open browser page  {pagePath}?auto=1&agentTaskId={taskId}&{param}=...&count=N
Page (user browser, logged in + extension) ──▶ POST /api/agent/scrape  (creates task with our taskId)
Extension executes scrape in TikTok tab
Page relays rows to server buffer
AI ──3. GET {SITE_URL}/api/agent/delivery/task/{taskId}/status  ──▶ {status:"ready"}
AI ──4. GET {SITE_URL}/api/agent/delivery/task/{taskId}/data    ──▶ CSV download
```

**Key invariant (v0.5):** the AI generates the taskId itself *before* opening the browser, so it never needs to read the browser address bar.

## Configuration

```text
BASE_URL       = https://monsterget.com      # API host (usually same as SITE_URL)
STATE_FILE     = ~/.monsterget/preflight-state.json   # persisted check results across conversations
```

`SITE_URL` (default: `https://monsterget.com`) — API host, same as `BASE_URL` in production.

Change `SITE_URL`/`BASE_URL` when the platform is running locally (`http://localhost:8000`).

**Link rule**: the user-facing links in Step 0 are written for production (`https://monsterget.com/install`, `https://monsterget.com`). If the platform runs locally, substitute the domain in those links with the configured `SITE_URL` — never show a bare `{SITE_URL}` placeholder to the user. Always produce a full, clickable URL.

### Browser variables and state persistence

These session variables are **set by Phase A of Step 0** and used everywhere (checks, scrapes, Step 3c/3c.1):

| Variable | Meaning |
|----------|---------|
| `BROWSER` | `edge` or `chrome` — which browser has the MonsterGet extension installed |
| `BROWSER_EXE` | `msedge` or `chrome` — for shell `start` / `tasklist` commands |
| `BROWSER_FULLPATH` | Full exe path for direct launch (fallback when `start` fails) |
| `EXT_OK` | `true` / `false` — extension check result |
| `MG_LOGIN_OK` | `true` / `false` — MonsterGet login check result |
| `TK_LOGIN_OK` | `true` / `false` — TikTok login check result |

**State file** (`$STATE_FILE`): a small JSON file persisted between conversations:

- **File**: `~/.monsterget/preflight-state.json`
- **Purpose**: (a) record of when the checks last passed, (b) `BROWSER` hint so a new conversation knows where to look. **It is NEVER a substitute for re-running the checks — every new conversation re-verifies.**
- **Contents**: `{browser, browser_exe, extension, monsterget_login, tiktok_login, checked_at}`
- **Rule**: each new conversation reads the file for the browser hint, then re-runs all checks and overwrites it. The file is kept only for reference and user visibility.

### Cold-start contract (crucial — read before any step)

**`PREFLIGHT_DONE` is `false` at the start of every new conversation.** Memory, prior conversations, and "I already told the user this before" must **never** set it.

**Verification is mandatory every session — but it does not have to cost the user anything.** Pick the entry path that matches what you actually know:

| Situation | Entry path | Cost to user |
|-----------|-----------|--------------|
| First time ever, or the user says they haven't set up | **Step 0** (interactive, step-by-step guidance + check) | ~2 min, once |
| Setup is presumed already done (your memory, a previous session, or the user says "already installed") | **Step 0.6** — silent programmatic preflight | **zero** — no questions asked |

Both paths end the same way: `PREFLIGHT_DONE=true`, only after checks actually pass. **There is no third path that skips verification.**

- Prior knowledge ("the extension was installed last week") ≠ this session has verified it. It selects **which** path you take, never **whether** you verify.
- If Step 0.6 fails, escalate to the Step 0 flow (start at the failed step) — do not proceed to a scrape.
- Never infer "verified" from the fact that a previous scrape succeeded. Every new conversation re-verifies.

**Key insight**: the check functions run programmatically, not by asking the user. "Don't bother the user" means "verify silently", never "skip verification".

## Scrape types

> ⚠️ **This table may be stale.** New scrapers are NOT auto-synced into this skill file. Before mapping the user's request to a type, fetch the live list (zero-auth, read-only) and use it if it differs from the table:
> ```bash
> curl -s {BASE_URL}/api/agent/scrapers
> ```
> Use the `type` + `page` + `param` + `countMax` values returned. The table below is a snapshot that matches current scrapers.

| Type | pagePath | Param | Default count | Max |
|------|----------|-------|---------------|-----|
| Video search | `/tiktok-search-video` | `query` | 50 | 300 |
| Creator search | `/tiktok-search-user` | `query` | 30 | 300 |
| Hashtag search | `/tiktok-tag` | `query` | 30 | 300 |
| Creator videos | `/tiktok-user-videos` | `username` | 50 | 300 |
| Creator profile | `/tiktok-profile` | `username` | 1 | 1 |

Username accepts `@name` or full profile URL (server normalizes).

## The full flow

> 🚨 **Flow — two entry paths, same destination**
>
> ```
> ┌────────────────────────────────────────────────────────────────────────┐
> │  First scrape of this session                                         │
> │     │                                                                 │
> │     ├── [Path A] No prior knowledge / user says not set up            │
> │     │     │                                                           │
> │     │     └── Step 0: pre-check all 3 → show status → guide ❌        │
> │     │           ① install extension  → _check_extension              │
> │     │           ② login monsterget   → _check_monsterget_login        │
> │     │           ③ login TikTok       → _check_target_login            │
> │     │           any ❌ → re-guide → re-verify (do NOT advance)        │
> │     │           all ✅ → PREFLIGHT_DONE=true → proceed to Step 1      │
> │     │                                                                 │
> │     ├── [Path B] Setup presumed done (memory / prior session)         │
> │     │     │                                                           │
> │     │     └── Step 0.6: silent programmatic preflight (calls checks)  │
> │     │           all pass → PREFLIGHT_DONE=true, continue              │
> │     │           any fail → escalate to Step 0 flow                   │
> │     │                                                                 │
> │     ├── Step 1~3: run the scrape normally                             │
> │     │                                                                 │
> │     └── after first success → subsequent scrapes this session         │
> │         skip Step 0/0.6 entirely, go straight to Step 1               │
> └────────────────────────────────────────────────────────────────────────┘
> ```

### ⚡ Automation contract (read this first)

**Opening the browser is fire-and-forget — but launching it is NOT.** Never pause to ask the user "is it open?" or "shall I continue?". Do **not** skip the silent process check in Step 3c.1 — "don't ask the user" means "verify programmatically instead", not "verify nothing".

Once you run the browser-open command, the page executes on its own — it creates the task with the taskId you already hold and the extension runs it. Your job is to *immediately* start polling. There is nothing to wait for from the user.

Rules that make the AI fast instead of slow:

1. **Open + verify + poll in one shot.** Run the browser-open command, the Step 3c.1 process check, and the poll loop together (see Step 3c). Do not put a message to the user between them.
2. **Never wait for user confirmation** after opening the browser. The user does not need to do anything (unless they aren't logged in yet — that's the one exception, and it shows up as the scrape never reaching `ready`).
3. **Polling already detects completion.** The poll loop exits the moment the status is `ready` (or `failed`). You do not need to ask the user whether the task finished — the status endpoint tells you.
4. **Multiple scrapes run back-to-back, unattended.** When the user asks for several scrapes, run them in a loop: open → verify → poll → download → open the next one. Do **not** stop and report back between tasks. See "Running multiple scrapes" below.
5. **A finished task frees the concurrency slot.** The scrape window may stay open — it does not block the next task. Only a task still `pending`/`processing` counts against the limit.
6. **Only speak to the user** when: first-time setup (Step 0), a scrape fails, or all requested scrapes are done and you're presenting results.

### Step 0 — 🚀 First-time setup: pre-check first, then guide what's missing (Path A only)

> **💡 SKIP RULE**: Step 0 runs only on **Path A** (no prior knowledge, or the user says setup isn't done). If you have prior knowledge the setup is already complete, go **Path B** — Step 0.6 only, no interactive flow. Once `PREFLIGHT_DONE=true` in this session, skip Steps 0/0.6 entirely for later scrapes.

> ⛔ **Setup is an interactive flow, NOT a notice.** Four hard rules:
>
> 1. **Never** present setup as a "reminder", "note", "things to know", "prerequisites", or a bullet list the user reads on their own.
> 2. **Never** print all three steps at once and wait for a single "done" — that is a checklist, not guidance.
> 3. **Never** echo the skill description, pricing, or quota as a lead-in "reminder" block.
> 4. **Always give a full, clickable URL** — `https://monsterget.com/install` (not a `{SITE_URL}` placeholder). The user must be able to click or paste it directly.
>
> Instead: **pre-check what's already done → report status → guide only the unfinished steps**, one at a time. The user must never have to guess whether a step worked — you verify it programmatically and tell them.

> 🔒 **Same-browser rule (critical)**: the extension, the MonsterGet login, and the TikTok login must all be in the **same browser**. The extension only works in the browser it's installed in. When guiding, always name the browser explicitly: "用 Edge" / "用 Chrome". Never let the user spread the three steps across two browsers.

#### Phase A — Silent pre-check (before telling the user anything)

**A1. Determine the browser first** (never guess, never silently default to Edge).

Read the state file for a browser hint (informational only — the actual check re-verifies), then run `_detect_browser()`:

```bash
# Load previous browser hint (not a substitute for detection)
if [ -f "$STATE_FILE" ]; then
  PREV_BROWSER=$(grep -o '"browser":"[^"]*"' "$STATE_FILE" | cut -d'"' -f4)
fi

# Actually detect which browser now has the extension
_detect_browser
```

**Then name the browser explicitly to the user** (never leave it unspecified):

| Detection result | What to tell the user |
|---------------- |-----------------------|
| `edge` | ✅ 扩展在 **Edge** 里，以下操作都用 Edge。 |
| `chrome` | ✅ 扩展在 **Chrome** 里，以下操作都用 Chrome。 |
| `none` | ❌ 还没检测到扩展，先安装扩展并确定用哪个浏览器。 |

**A2. Run the 3 short-probe checks** against the detected browser (poll only 3×5s per login check — enough to detect an already-finished setup). If `BROWSER=none`, skip checks and go directly to Phase B Step ① (after extension is installed, the check after Step ① detects the browser).

**A3. Show the status table in the user's language, naming the browser**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  准备情况检查（浏览器：${BROWSER}）
  ① 安装 MonsterGet 扩展     ✅ / ❌ 未安装
  ② 登录 monsterget.com     ✅ 已登录 / ❌ 未登录
  ③ 登录 TikTok             ✅ 已登录 / ❌ 未登录
  提示：3 项都用同一个浏览器（${BROWSER}）操作。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Set session variables: `EXT_OK`, `MG_LOGIN_OK`, `TK_LOGIN_OK` based on results.

**A4. Enter Phase B** — guide only the rows marked ❌, in order ①→②→③. Rows already ✅ are skipped silently — do not ask the user to redo them.

#### The per-step protocol (for each unfinished step)

```
for each unfinished step, in order:
  1. TELL    one short message: what to do + the FULL clickable URL + which browser
  2. WAIT    wait for the user to say they're done — never advance early
  3. VERIFY  run THAT step's check function (library below) — programmatically
  4. REPORT  "✅ Step N done" or "❌ Step N failed: <exactly how to fix>"
  5. if ❌   → re-guide → wait → re-verify. Loop until ✅. Do NOT advance.
  → next unfinished step
```

All three ✅ (from pre-check or guidance) → `PREFLIGHT_DONE=true` → tell the user setup is complete → Step 1.

#### Step ① — Install the MonsterGet browser extension

**TELL** — pick the wording based on what Phase A detected:

*If the extension was already detected* (`BROWSER=edge|chrome`):
> **第 1 步 — 扩展已就绪**
> 已检测到 MonsterGet 扩展在 **{BROWSER}** 里，无需重装。
> 后续 2 步都会用 **{BROWSER}**。

*If not detected* (`BROWSER=none`):
> **第 1 步 — 安装 MonsterGet 扩展**
> 打开安装页：**https://monsterget.com/install**
> 把扩展装到 **Edge 或 Chrome**（选一个，后面 3 步都用它）。
> 装好后回复"好了，用 Edge"或"好了，用 Chrome"，我会检测并确认浏览器。

**VERIFY**: re-run `_detect_browser()` (the extension may have just been installed, so `BROWSER` can change from `none`), then `_check_extension` → `ok` | `missing`

| Result | REPORT | Next |
|--------|--------|------|
| `ok` | "✅ 第 1 步完成：扩展已安装在 **{BROWSER}** 里。" | → next unfinished step |
| `missing` | "❌ 还没检测到扩展。请确认：① 扩展装好了吗？② 装在了 Edge 还是 Chrome？③ 装完后刷新过 https://monsterget.com/install 吗？装好后回复'好了'。" | re-guide → wait → re-verify |

> 🔁 **After a successful detection, state the browser once more in the next step's message** — so the user never has to remember which browser they picked.

**🚧 Blocking rule**: while ① is `missing`, do **not** advance to ② or ③ — both logins must happen in the browser that has the extension.

#### Step ② — Log in to monsterget.com

**TELL** — always name the browser (replace `{BROWSER}` with the actual name):

> **第 2 步 — 登录 monsterget.com（用同一个浏览器：{BROWSER}）**
> 打开：**https://monsterget.com**
> 注册或登录你的账号（游客登录也可以）。
> 完成后回复"好了"，我会自动检测登录状态。

**VERIFY**: `_check_monsterget_login` → polls up to 60s (12 × 5s)

| Result | REPORT | Next |
|--------|--------|------|
| `logged_in: true` | "✅ 第 2 步完成：已登录 monsterget.com。" | → next unfinished step |
| `false` (timeout) | "❌ 还没有检测到登录。请确认是在刚才安装扩展的同一个浏览器（{BROWSER}）里打开了 https://monsterget.com 并登录，然后回复'好了'。" | re-guide → wait → re-verify |

> Before the check opens the browser, apply the Step 3c.1 rule: confirm the process actually started. A silent `start` failure looks exactly like "not logged in", and will send you chasing the wrong problem.

#### Step ③ — Log in to TikTok

**TELL** — always name the browser (replace `{BROWSER}`):

> **第 3 步 — 登录 TikTok（用同一个浏览器：{BROWSER}）**
> 打开：**https://www.tiktok.com**
> 登录你的 TikTok 账号。
> （如果只抓取非 TikTok 平台，此步可跳过。）
> 完成后回复"好了"，我会自动检测。

**VERIFY**: `_check_target_login` → polls up to 60s (12 × 5s)

| Result | REPORT | Next |
|--------|--------|------|
| `logged_in: true` | "✅ 第 3 步完成：已登录 TikTok。" | all three ✅ → setup complete |
| `false` (timeout) | "❌ 还没有检测到 TikTok 登录。请确认是在同一个浏览器（{BROWSER}）里登录的，然后回复'好了'。" | re-guide → wait → re-verify |

#### Browser detection + check functions (library)

> **Run `_detect_browser()` FIRST, before any other check.** It sets `BROWSER`, `BROWSER_EXE`, `BROWSER_FULLPATH`. Every check below then uses those variables — never a hardcoded `msedge`. If you skip detection, you will check the wrong browser and mislead the user.

```bash
# Browser detection — scans both browsers, returns which one has the extension.
# Sets the session variables below. Run BEFORE any other check.
_detect_browser() {
  EDGE_PREF="$HOME/AppData/Local/Microsoft/Edge/User Data/Default/Preferences"
  CHROME_PREF="$HOME/AppData/Local/Google/Chrome/User Data/Default/Preferences"
  if [ -f "$EDGE_PREF" ] && grep -q "MonsterGet" "$EDGE_PREF" 2>/dev/null; then
    BROWSER="edge"; BROWSER_EXE="msedge"
    BROWSER_FULLPATH="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
  elif [ -f "$CHROME_PREF" ] && grep -q "MonsterGet" "$CHROME_PREF" 2>/dev/null; then
    BROWSER="chrome"; BROWSER_EXE="chrome"
    BROWSER_FULLPATH="/c/Program Files/Google/Chrome/Application/chrome.exe"
  else
    BROWSER="none"; BROWSER_EXE=""; BROWSER_FULLPATH=""
  fi
  echo "$BROWSER"
}
```

```bash
# ① Extension install check — uses BROWSER from _detect_browser
#    Returns: ok | missing
_check_extension() {
  if [ "$BROWSER" = "edge" ] || [ "$BROWSER" = "chrome" ]; then echo "ok"; else echo "missing"; fi
}
```

```bash
# ② MonsterGet login check (needs a browser page to report back)
#    Uses $BROWSER_EXE / $BROWSER_FULLPATH — same browser as the extension.
_check_monsterget_login() {
  local MG_ID=$(curl -s "$BASE_URL/api/agent/generate-task-id" | sed -n 's/.*"taskId":"\([^"]*\)".*/\1/p')
  if command -v "$BROWSER_EXE" >/dev/null 2>&1; then
    start "$BROWSER_EXE" "$SITE_URL/login-check.html?auto=1&agentTaskId=$MG_ID"
  else
    "$BROWSER_FULLPATH" "$SITE_URL/login-check.html?auto=1&agentTaskId=$MG_ID"
  fi
  for i in $(seq 1 12); do
    local R=$(curl -s "$BASE_URL/api/agent/login-check/$MG_ID")
    echo "$R" | grep -q '"logged_in"' && { echo "$R"; return; }
    sleep 5
  done
  echo '{"logged_in":false}'
}
```

```bash
# ③ Target-site (TikTok) login check (needs a browser page to report back)
#    Uses $BROWSER_EXE / $BROWSER_FULLPATH — same browser as the extension.
_check_target_login() {
  local T=$(curl -s -X POST "$BASE_URL/api/agent/login-check-target" \
    -H "Content-Type: application/json" -d '{"target":"tiktok"}')
  local TK_ID=$(echo "$T" | sed -n 's/.*"taskId":"\([^"]*\)".*/\1/p')
  if command -v "$BROWSER_EXE" >/dev/null 2>&1; then
    start "$BROWSER_EXE" "$SITE_URL/login-check-target.html?auto=1&agentTaskId=$TK_ID&target=tiktok"
  else
    "$BROWSER_FULLPATH" "$SITE_URL/login-check-target.html?auto=1&agentTaskId=$TK_ID&target=tiktok"
  fi
  for i in $(seq 1 12); do
    local R=$(curl -s "$BASE_URL/api/agent/login-check/$TK_ID")
    echo "$R" | grep -q '"logged_in"' && { echo "$R"; return; }
    sleep 5
  done
  echo '{"logged_in":false}'
}
```

#### Retry rules (same per-step loop, when a step fails)

1. **Never advance past a failed step.** Only the step that failed is re-checked; steps that already passed are not re-run.
2. **Poll timeout**: 60 seconds max per browser-based check (12 × 5s). Timeout counts as fail.
3. **User wait**: after opening the browser for a check, poll immediately — don't interrupt the user. Only speak when reporting ✅/❌.
4. **Blocking**: if ① (extension) is `missing`, do not attempt ② or ③.

#### Completion

After all three steps pass, tell the user (in their language):

> ✅ 全部准备完成！开始抓取...

Then save the result to the state file and set the session flag:

```bash
mkdir -p "$(dirname "$STATE_FILE")"
cat > "$STATE_FILE" << EOFSTATE
{
  "browser": "${BROWSER:-edge}",
  "browser_exe": "${BROWSER_EXE:-msedge}",
  "extension": ${EXT_OK:-false},
  "monsterget_login": ${MG_LOGIN_OK:-false},
  "tiktok_login": ${TK_LOGIN_OK:-false},
  "checked_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOFSTATE
```

Then set `PREFLIGHT_DONE=true` (session variable) and go to Step 1. Subsequent scrapes in this session skip Steps 0/0.6 entirely.

#### State persistence rules (re-check every conversation)

1. **Every new conversation reads** `$STATE_FILE` (if it exists) for the browser hint and the last check timestamp. This is informational only — it helps you tell the user "上次检查通过于 2026-09-12" and which browser.
2. **Every new conversation re-runs** all checks in Phase A. The saved results are authority only for the user's visibility, never for skipping verification.
3. **Never skip Phase A** because the state file says everything was OK. `PREFLIGHT_DONE` is always `false` at session start — cold-start contract.
4. After re-checking, **overwrite** the state file with fresh results and timestamp.

### Step 0.6 — 🪄 Silent preflight (programmatic, ~20 seconds)

> **Path B entry** — use when you have prior knowledge the setup is already done (memory, a previous session, or the user says "already installed"). Runs checks programmatically. **If in doubt about the setup state, run Step 0 (Path A) instead.**

A silent programmatic check — no user interaction required, no questions asked.  
If all pass → `PREFLIGHT_DONE=true`, proceed to Step 1. If any fail → escalate to the user with the Step 0 flow (start at the failed step's TELL).

```bash
# 0. Detect the browser FIRST (never assume Edge)
_detect_browser   # sets BROWSER, BROWSER_EXE, BROWSER_FULLPATH

# ① Extension install check (local file scan, 0.1s, no browser needed)
EXT_RESULT=$(_check_extension)   # defined in Step 0
if [ "$EXT_RESULT" = "missing" ]; then
  echo "FAIL: extension not found"
  # → escalate to Step 0 ① (interactive). Do NOT proceed to a scrape.
fi

# ② MonsterGet reachability (API probe, 1s)
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/agent/generate-task-id")
if [ "$HTTP_CODE" != "200" ]; then
  echo "FAIL: platform unreachable (HTTP $HTTP_CODE)"
  # → tell user platform isn't reachable, stop. Do NOT proceed to a scrape.
fi

# ③ Browser launch + login check — generate taskId, open a login-check page, poll
#    Uses $BROWSER_EXE / $BROWSER_FULLPATH (same browser as the extension)
TASK_ID=$(curl -s "$BASE_URL/api/agent/generate-task-id" | sed -n 's/.*"taskId":"\([^"]*\)".*/\1/p')
if command -v "$BROWSER_EXE" >/dev/null 2>&1; then
  start "$BROWSER_EXE" "$SITE_URL/login-check.html?auto=1&agentTaskId=$TASK_ID"
else
  "$BROWSER_FULLPATH" "$SITE_URL/login-check.html?auto=1&agentTaskId=$TASK_ID"
fi
# verify the browser process started (same rule as Step 3c.1)
sleep 3
if tasklist /fi "IMAGENAME eq $BROWSER_EXE.exe" 2>/dev/null | grep -q "$BROWSER_EXE"; then
  echo "OK: browser started"
else
  echo "FAIL: browser did not start — retry with full exe path (see Step 3c.1)"
fi

LOGIN_OK="false"
for i in 1 2 3; do
  RESULT=$(curl -s "$BASE_URL/api/agent/login-check/$TASK_ID")
  echo "$RESULT" | grep -q '"logged_in"' && { LOGIN_OK="true"; break; }
  sleep 2
done
if [ "$LOGIN_OK" != "true" ]; then
  echo "FAIL: not logged in"
  # → escalate to Step 0 ② (interactive login guidance), stop
fi
```

**On failure**: escalate to the interactive Step 0 flow, starting at the step that failed. Wait for the user's "done", then re-verify (via the step's check, not the whole 0.6).

**On success**: set `PREFLIGHT_DONE=true` (and `SESSION_PREFLIGHT_PASSED=true`). Subsequent scrapes this session skip Steps 0/0.6 entirely.

### Step 1 — Platform reachability check

> 💡 If `PREFLIGHT_DONE=true` (set by Step 0 or Step 0.6), this is the **first step** for this scrape — Steps 0/0.6 are skipped.

Quickly probe whether the platform is reachable:

```bash
# Reachability
curl -s -o /dev/null -w "%{http_code}" {BASE_URL}/api/agent/generate-task-id
```

- `200` → reachable. Continue.
- Anything else → tell the user the platform isn't reachable yet. For local: ask them to start the backend. Then stop.

If scraping previously failed with an extension error, ask the user to verify the extension is installed and the browser is logged in (see Troubleshooting).

### Step 2 — First-time setup (folded into Step 0)

> ✅ The first-time guide was completed in Step 0. Not repeated here.
>
> If the user reports a missing extension or login problem, refer to Step 0's per-step guidance:
> - Install extension: https://monsterget.com/install
> - Log in to MonsterGet: https://monsterget.com
> - Log in to the target site (TikTok): https://www.tiktok.com

### Step 3 — Run a scrape (repeatable)

#### 3a. Generate a taskId (zero-auth, no token needed)

```bash
TASK_ID=$(curl -s {BASE_URL}/api/agent/generate-task-id | sed -n 's/.*"taskId":"\([^"]*\)".*/\1/p')
echo "taskId=$TASK_ID"
```

Keep this id — it is the key for everything that follows.

#### 3b. Determine page and params from the user's request

Map intent → `{pagePath}?auto=1&agentTaskId={TASK_ID}&{param}={value}&count={N}`:

| User intent | pagePath | param |
|-------------|----------|-------|
| "videos about X" / "search X" | `/tiktok-search-video` | `query=X` |
| "TikTok users/creators doing X" | `/tiktok-search-user` | `query=X` |
| "#tag videos" / "topic X" | `/tiktok-tag` | `query=X` (drop the `#`) |
| "videos by @creator" | `/tiktok-user-videos` | `username=@creator` |
| "profile of @creator" | `/tiktok-profile` | `username=@creator` |

If count isn't given, use the type default (30 for tag/user search, 50 for video/user-videos). Cap at 300. Path segment separator is a **hyphen** (`/tiktok-search-video`), never an underscore.

#### 3c. Open the page in the chosen browser — **fire-and-forget**

⚠️ **URL must be wrapped in double quotes** — otherwise the shell treats `&` as a command separator and truncates the query.

> 🚀 **Before you open the browser**: run `_detect_browser()` (Step 0.6) to set `BROWSER` / `BROWSER_EXE` / `BROWSER_FULLPATH`. Every command below uses these variables — never hardcode a browser name.

```bash
# Open in the detected browser (Windows — works for edge or chrome)
# Uses $BROWSER_EXE — whichever browser the extension is installed in
start "$BROWSER_EXE" "https://monsterget.com/tiktok-search-video?auto=1&agentTaskId=$TASK_ID&query=mike&count=10"
```

If `start` isn't available, use the full exe path:
```bash
"$BROWSER_FULLPATH" "https://monsterget.com/tiktok-search-video?auto=1&agentTaskId=$TASK_ID&query=mike&count=10"
```

> 🚀 **Do NOT ask the user** "is it open?" after opening the browser. Do not pause, do not read the URL bar. The page creates the task with the taskId you already hold and runs automatically.
>
> ⚠️ **But DO verify the browser process actually started** before pollling (Step 3c.1). The open command can fail silently (e.g. `$BROWSER_EXE` not in PATH in Git Bash). If the browser never started, every poll will return `not_found`. Verify programmatically — never by asking the user.

#### 3c.1 — Verify the browser process started (new, read this)

After the open command, immediately verify the process exists — **do not ask the user**:

```bash
# Wait up to 3 seconds for the process to appear
# $BROWSER_EXE was set by _detect_browser() — the browser that has the extension
BROWSER_STARTED=false
for i in 1 2 3; do
  if tasklist /fi "IMAGENAME eq $BROWSER_EXE.exe" 2>/dev/null | grep -qi "$BROWSER_EXE"; then
    BROWSER_STARTED=true
    echo "✅ browser process confirmed ($BROWSER_EXE.exe)"
    break
  fi
  sleep 1
done
```

**If `BROWSER_STARTED=false`**: the `start` command failed silently. Try the full exe path explicitly — using the path that `_detect_browser()` already found:

```bash
# Retry with the full path of the detected browser
"$BROWSER_FULLPATH" "{URL}"

# Re-check after retry
sleep 2
if tasklist /fi "IMAGENAME eq $BROWSER_EXE.exe" 2>/dev/null | grep -qi "$BROWSER_EXE"; then
  echo "✅ browser started via full path"
  BROWSER_STARTED=true
fi
```

> If `$BROWSER_FULLPATH` doesn't exist either, fall back to the canonical paths for the detected browser:
> ```bash
> # Edge
> "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" "{URL}"
> # Chrome
> "/c/Program Files/Google/Chrome/Application/chrome.exe" "{URL}"
> ```
> Do NOT blindly try the other browser — the extension only exists in one of them (that's what `_detect_browser` determined). Opening the wrong browser creates a task that can never complete.

**If still not running after full-path retry**: stop and tell the user "I tried to open the browser but the process did not start. Please open `{URL}` manually in the browser where the extension is installed, then reply 'done'."

**If confirmed running**: proceed to Step 3d immediately. No user message needed.

#### 3d. Poll until ready — **start immediately, start in the background**

Open the browser **and start polling in the same step**. Use your tool's run_in_background feature for the poll loop so it works while you can still interact with the user (or start the next task in serial mode):

```bash
# Bash / Mac / Linux — poll every 5s, up to 60 times (5-minute timeout)
for i in $(seq 1 60); do
  STATUS=$(curl -s "https://monsterget.com/api/agent/delivery/task/$TASK_ID/status")
  echo "$STATUS" | grep -q '"status":"ready"' && break
  echo "$STATUS" | grep -qE '"status":"(downloaded|failed)"|not_found' && break
  sleep 5
done
```

```bat
:: Windows cmd — poll every 5s, up to 60 times (5-minute timeout)
for /l %i in (1,1,60) do (
  curl -s "https://monsterget.com/api/agent/delivery/task/$TASK_ID/status" | find "ready"
  if not errorlevel 1 goto download
  timeout /t 5 /nobreak >nul
)
:download
```

Status meanings:
| status | meaning |
|--------|---------|
| `processing` | still running → keep polling |
| `ready` | data ready → download |
| `downloaded` | already fetched → can't re-download |

Response example: `{"taskId":"...","status":"ready","filename":"mike-10-20260905_tiktok_video_ab12cd.csv","resultCount":10,"terminal":true}`

#### 3e. Download the CSV

```bash
curl -OJ "https://monsterget.com/api/agent/delivery/task/$TASK_ID/data"
```

`-OJ` uses the server's semantic filename (`Content-Disposition`). The file is tombstoned after one download (repeat → HTTP 410). Download is only available for 24h.

#### 3f. Verify & present

Show the user the first rows of the CSV so they can confirm the data is correct. State the saved file path.

### Step 4 — Bulk creator profiles (optional)

When the user needs profile data for **multiple creators at once** (e.g., "get profiles of @mike, @jenifer, @tiktok"), use bulk mode with comma-separated usernames:

```bash
TASK_ID=$(curl -s {BASE_URL}/api/agent/generate-task-id | sed -n 's/.*"taskId":"\([^"]*\)".*/\1/p')
start "$BROWSER_EXE" "https://monsterget.com/tiktok-profile?auto=1&agentTaskId=$TASK_ID&usernames=mike,jenifer,tiktok&count=3"
```

The platform creates a **parent task** that chains through each profile sequentially. Poll and download using `$TASK_ID` — the CSV contains one row per creator with aggregated profile stats.

### Running multiple scrapes (serial batch)

When the user asks for **several scrapes at once** (e.g. "test all 5 scrapers"), run them **back-to-back in a loop, unattended**:

```
1. TASK_ID = generate-task-id
2. open browser page 1          (fire-and-forget)
3. verify browser process       (Step 3c.1 — programmatic only)
4. poll until ready             (background)
5. download CSV 1
6. TASK_ID = generate-task-id
7. open browser page 2          ← do NOT wait for the user between tasks
8. verify browser process       (same silent check)
9. poll → download
... repeat ...
```

Key rules:
- **Do not stop to ask the user between tasks.** Each new scrape is independent and the concurrency slot frees as soon as the previous one is `ready`.
- The old browser tab may stay open — **it does not block anything**. Close tabs only if you want to reduce clutter.
- Only **serialize if the user has 1 concurrent window** (free tier). If you get a `429 too_many_concurrent_scrapes`, it means a previous task is still `pending`/`processing` — wait for it to be `ready`/`failed`, then continue.
- Report all results **at the end**, together, not one at a time.

## Error handling

| Symptom | Cause | Fix |
|---------|-------|-----|
| `curl` returns nothing / connection refused | platform not reachable | confirm backend running (local) or site is up (production) |
| status endpoint → `404 delivery_not_found` (transient, <60s) | wrong taskId | re-run 3a and regenerate |
| `delivery_not_found` **persists >60s** | **browser never started** — the open command silently failed (exe not in PATH), so the page never created the task | Verify with `tasklist /fi "IMAGENAME eq $BROWSER_EXE.exe"`; retry with `$BROWSER_FULLPATH` (Step 3c.1); if still absent, ask user to open the URL manually |
| status stays `processing` > 5 min | extension missing, browser not logged in, or page closed | confirm extension installed + logged in + page still open; page must stay open until scrape completes |
| status endpoint never reaches `ready`, page shows "extension not ready" | extension not installed / not enabled | install extension from https://monsterget.com/install, reload page |
| page shows "please log in" | not logged in | log in on https://monsterget.com, reopen page |
| Step 0 check ③ TikTok login failed | browser not logged into TikTok | log into TikTok, reply "done", AI re-checks |
| download → `409 not_ready` | data not ready | keep polling |
| download → `409 buffer_unavailable` | buffer cleared by TTL race | retry a few seconds |
| download → `410 already_downloaded` | already fetched once | do NOT retry; regenerate a taskId and run a new scrape |
| 429 too_many_concurrent_scrapes | a previous task is still pending/processing | free users have 1 concurrent window — wait for the running task to reach `ready`/`failed`, then retry. Closing the browser tab is NOT required; a finished task already frees the slot |
| 402 insufficient_credits | credits exhausted | signup grants 10M credits — almost never runs out; need more? contact the platform |

## Concurrency note

Free-tier users have **1 concurrent scrape window** (plenty for daily use). Member tiers can run **up to 10 in parallel**.

The limit counts **running tasks**, not open windows:
- A task counts while it is `pending` or `processing` (the extension is still working).
- The moment a task reaches `ready`, the slot is **freed** — you can open the next scrape right away.
- **An open browser tab with a finished task does NOT block the next task.** Leave tabs open; there is no need to close them.
- A `pending` task that was never claimed (extension not ready / page abandoned) auto-expires after ~30 seconds.

## Gotchas

- **Use the extension-installed browser.** Never rely on the system default browser — it may not have the extension. Ask once, remember the answer.
- **Never call `POST /api/agent/scrape` yourself.** The page does it automatically with your taskId. Calling it manually is not needed and requires auth.
- **Never run headless / sandbox scraping.** Scrapes execute in the user's real browser for anti-ban. If you're sandboxed and can't open a local browser, tell the user to run a local AI terminal (Claude Code CLI, local Codex).
- **Keep the tab open** until the task reaches `ready`. Closing the tab before the extension reports results means no server copy is produced.
- **Do not wait for the user between scrapes.** Open → poll → download → next, all in one uninterrupted run.
- After downloading, show the user the CSV path and a preview so they trust the result.

## Sources

- Platform: [monsterget.com](https://monsterget.com)
- Skill repository: [github.com/rosstzc/monsterget.com-skills](https://github.com/rosstzc/monsterget.com-skills)

---

## Appendix — zh-CN localized user-facing copy

> Use the Chinese wording below **only** when the user writes to you in Chinese. For all other languages, translate the English text in the body yourself. Never show this appendix to the user.

### Step 0 messages (中文)

> Send these **one at a time** — never all three at once. Links must be the **full URL**, never a `{SITE_URL}` placeholder.

**Phase A — 预检状态表**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  准备情况检查
  ① 安装 MonsterGet 扩展     ✅ 已完成 / ❌ 未安装
  ② 登录 monsterget.com     ✅ 已登录 / ❌ 未登录
  ③ 登录 TikTok             ✅ 已登录 / ❌ 未登录
  提示：3 项都必须在同一个浏览器里完成。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

只引导标 ❌ 的项，顺序 ① → ② → ③。已是 ✅ 的项直接跳过，不要让用户重做。

**① 安装扩展 — TELL**

```
第 1 步 — 安装 MonsterGet 扩展（用 Edge，或 Chrome）
打开安装页：https://monsterget.com/install
按页面指引把扩展安装到 Edge（或 Chrome）。
装好后回复"好了"，我会自动检测。
```

- ✅ `✅ 第 1 步完成：扩展已安装。`
- ❌ `❌ 还没有检测到扩展。请确认：① 是装在了 Edge 或 Chrome 里吗？（就是刚才打开安装页的那个浏览器）② 装完后刷新过 https://monsterget.com/install 页面吗？装好后回复"好了"。`

**② 登录 monsterget.com — TELL**

```
第 2 步 — 登录 monsterget.com（用同一个浏览器：Edge）
打开：https://monsterget.com
注册或登录你的账号（游客登录也可以）。
完成后回复"好了"，我会自动检测登录状态。
```

- ✅ `✅ 第 2 步完成：已登录 monsterget.com。`
- ❌ `❌ 还没有检测到登录。请确认是在刚才安装扩展的同一个浏览器（Edge）里打开了 https://monsterget.com 并登录，然后回复"好了"。`

**③ 登录 TikTok — TELL**

```
第 3 步 — 登录 TikTok（用同一个浏览器：Edge）
打开：https://www.tiktok.com
登录你的 TikTok 账号。
（如果只抓取非 TikTok 平台，此步可跳过。）
完成后回复"好了"，我会自动检测。
```

- ✅ `✅ 第 3 步完成：已登录 TikTok。`
- ❌ `❌ 还没有检测到 TikTok 登录。请确认是在同一个浏览器（Edge）里登录的，然后回复"好了"。`

**全部完成**

`✅ 全部准备完成！开始抓取...`
