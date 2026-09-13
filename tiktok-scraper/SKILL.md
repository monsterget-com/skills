---
name: tiktok-scraper
description: 🎁 Permanently free — 10M entries on signup, 1 concurrent window. Zero-install skill: open a browser URL, the extension + logged-in session do the rest. TikTok video search, creator discovery, hashtag collection, user video export to CSV. Works with Claude Code, Codex, Cursor, Windsurf, Cline, ChatGPT (any AI client). No Python packages, no credentials, no headless setup.
---

# TikTok Scraper

> 🎁 **Permanently free · 10 million entries on signup · 1 concurrent window for free users**
> *(Members unlock more parallel windows.)*

## What is this?

A skill that lets **any AI assistant** (Claude Code, Codex, Cursor, Windsurf, Cline, ChatGPT…) scrape TikTok data — video search, creator discovery, hashtag collection, or a specific creator's videos — and return it as a CSV. You don't install Python packages, configure headless browsers, or manage credentials. The AI orchestrates: it generates a task ID, opens a URL in the **user's own browser**, and downloads the result.

**Why a browser + extension?** The actual scrape runs inside the user's real TikTok session (logged in, with the [MonsterGet](https://monsterget.com) browser extension installed). That's what keeps the accounts anti-ban safe. There is no server-side TikTok scraping — the data is collected right where the user is already logged in.

**First-time setup (one-time, ~2 minutes):** the user registers a free account at [monsterget.com](https://monsterget.com) and installs the extension (Chrome/Edge). Everything after that is repeatable and instant.

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
AI ──1. GET {BASE_URL}/api/agent/generate-task-id ──▶ {"taskId":"<uuid>"}
AI ──2. open browser page  {pagePath}?auto=1&agentTaskId={taskId}&{param}=...&count=N
Page (user browser, logged in + extension) ──▶ POST /api/agent/scrape  (creates task with our taskId)
Extension executes scrape in TikTok tab
Page relays rows to server buffer
AI ──3. GET {BASE_URL}/api/agent/delivery/task/{taskId}/status  ──▶ {status:"ready"}
AI ──4. GET {BASE_URL}/api/agent/delivery/task/{taskId}/data    ──▶ CSV download
```

**Key invariant:** the AI generates the taskId itself *before* opening the browser, so it never needs to read the browser address bar.

## Configuration

```text
BASE_URL   = https://monsterget.com      # API host (usually same as SITE_URL)
SITE_URL   = https://monsterget.com      # page host
STATE_FILE = ~/.monsterget/state.json    # persisted check results + browser hint
```

Override for a local platform via environment variables: `MONSTERGET_BASE_URL=http://localhost:8000` (and optionally `MONSTERGET_SITE_URL`, `MONSTERGET_STATE_DIR`).

**Link rule**: the user-facing links in Step 0 are written for production (`https://monsterget.com/install`, `https://monsterget.com`). If the platform runs locally, substitute the domain in those links with the configured `SITE_URL` — never show a bare `{SITE_URL}` placeholder to the user. Always produce a full, clickable URL.

## 🧩 Scripts — the runtime (read this before any step)

**All shell work is delegated to four protocoled scripts.** Do not re-implement browser detection, process checks, or polling inline — that was the old design and it broke (shell state doesn't survive between tool calls, and the inline code was Windows-only).

**Resolve the scripts directory once, at the start of the session, and reuse it:**

```bash
# Canonical shared-runtime path (recommended — works with all clients)
SCRIPTS="$HOME/.monsterget/skill/scripts"

# If not found, the skill needs installing — stop here and tell the user.
# (For development: point SCRIPTS at your local clone's scripts/ directory.)
if [ ! -d "$SCRIPTS" ]; then
  echo "Skill not installed: run the install instruction first." >&2
  echo "SCRIPTS=$SCRIPTS" >&2
  exit 1
fi
echo "SCRIPTS=$SCRIPTS"
```

Every command below is written as `bash "$SCRIPTS/<name>.sh"`.

| Script | What it does | Exit code |
|--------|--------------|-----------|
| `detect-browser.sh` | Finds **every** browser holding the MonsterGet extension. Writes `browser`, `browsers`, `browser_exe`, `browser_fullpath`, `os`, `extension`, `multiple`, `need_choice` to state. | 0 = found, 1 = not found |
| `choose-browser.sh <edge\|chrome>` | Saves the user's browser choice (`browser_pref`) — call only after asking, when `need_choice:true`. | 0 = saved, 1 = refused |
| `check-login.sh <monsterget\|tiktok>` | Opens the platform's login-check page, polls up to 60s (or `MONSTERGET_POLLS` × 5s). Writes the login result to state. | 0 = logged in, 1 = not |
| `preflight.sh` | Silent full preflight: extension → browser choice → platform reachability → both logins. Short 3×5s login probes. | 0 = all pass, 1 = something failed |
| `run-scrape.sh <pagePath> <param> <value> [count]` | End-to-end scrape: taskId → open browser → verify process → poll → download CSV. | 0 = CSV downloaded, 1 = failed |
| `set-download-dir.sh [<dir>]` | Choose where scraped CSVs are saved (persisted in state). No arg = the OS default Downloads dir. | 0 = saved, 1 = cannot create dir |

**Every script prints exactly one JSON object to stdout.** Parse that — it is the authoritative result. Do not ask the user what happened.

### 🌐 Browser selection (which browser to use)

`detect-browser.sh` scans **both** Edge and Chrome and reports every browser that has the extension:

| Field | Meaning |
|-------|---------|
| `browser` | The chosen browser (`edge`/`chrome`/`none`) |
| `browsers` | **All** browsers that have the extension, e.g. `["edge","chrome"]` |
| `multiple` | `true` when more than one browser has the extension |
| `chosen_by` | `preference` (user already picked) \| `default` (script picked the first) \| `only_one` |
| `need_choice` | `true` → **you must ask the user which browser to use** |

Rules:

1. **One browser has the extension** → use it, no question asked.
2. **Several have it and the user already chose** (`chosen_by:"preference"`) → reuse the saved choice (`browser_pref` in state). No question.
3. **Several have it and no choice saved** (`need_choice:true`) → ask the user **once**, in their language: *"两个浏览器都装了 MonsterGet 扩展，你想用哪个？Edge 还是 Chrome？"* Then run `bash "$SCRIPTS/choose-browser.sh" edge` (or `chrome`) and continue.
4. **Never guess in this case.** Both `preflight.sh` (`next:"choose_browser"`) and `run-scrape.sh` (`status:"need_browser_choice"`) refuse to proceed — that's the gate. Asking is required, not optional.

The choice is persisted, so the question is asked **at most once per machine**, not every session.

**Why scripts instead of inline shell:** each script is self-contained (reads `state.json` → does work → writes `state.json`), so nothing depends on shell variables surviving between tool calls. And they branch on the OS, so they work on Windows (Git Bash), macOS, and Linux alike.

### State file (`~/.monsterget/state.json`)

A small JSON key/value store persisted between conversations:

```json
{"os":"windows","browser":"edge","browser_exe":"msedge","extension":"true",
 "monsterget_login":"true","tiktok_login":"true","checked_at":"2026-09-13T10:00:00Z"}
```

- **Purpose**: (a) a record of when the checks last passed, (b) a browser hint so a new conversation knows where to look, (c) the last taskId/URL, (d) the chosen CSV download dir (set via `set-download-dir.sh`).
- **It is NEVER a substitute for re-running the checks — every new conversation re-verifies.**
- The scripts read and write this file themselves. You generally don't need to touch it directly (though `cat ~/.monsterget/state.json` is a fine way to see the last known status).

## Cold-start contract (crucial — read before any step)

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

**Key insight**: the check scripts run programmatically, not by asking the user. "Don't bother the user" means "verify silently", never "skip verification".

## Scrape types

> ⚠️ **This table may be stale.** New scrapers are NOT auto-synced into this skill file. Before mapping the user's request to a type, fetch the live list (zero-auth, read-only) and use it if it differs from the table:
> ```bash
> curl -s "$BASE_URL/api/agent/scrapers"
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
> │     │           ① install extension  → detect-browser.sh             │
> │     │           ② login monsterget   → check-login.sh monsterget      │
> │     │           ③ login TikTok       → check-login.sh tiktok          │
> │     │           any ❌ → re-guide → re-verify (do NOT advance)        │
> │     │           all ✅ → PREFLIGHT_DONE=true → proceed to Step 1      │
> │     │                                                                 │
> │     ├── [Path B] Setup presumed done (memory / prior session)         │
> │     │     │                                                           │
> │     │     └── Step 0.6: preflight.sh (silent)                         │
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

**Opening the browser is fire-and-forget — but launching it is NOT.** Never pause to ask the user "is it open?" or "shall I continue?". The `run-scrape.sh` script already verifies the process started programmatically — do not skip that by not reading its output.

Once the script opens the browser, the page executes on its own — it creates the task with the taskId the script already generated and the extension runs it. The script polls immediately.

Rules that make the AI fast instead of slow:

1. **Run the scrape script once and let it do everything.** It opens, verifies, polls, and downloads in a single call. Do not split it into separate commands.
2. **Never wait for user confirmation** after opening the browser. The user does not need to do anything (unless they aren't logged in yet — that's the one exception, and it shows up as the scrape never reaching `ready`).
3. **Polling already detects completion.** The script exits the moment the status is `ready` (or `failed`). You do not need to ask the user whether the task finished.
4. **Multiple scrapes run back-to-back, unattended.** Call the script in a loop — do **not** stop and report back between tasks. See "Running multiple scrapes" below.
5. **A finished task frees the concurrency slot.** The scrape window may stay open — it does not block the next task. Only a task still `pending`/`processing` counts against the limit.
6. **Only speak to the user** when: first-time setup (Step 0), a scrape fails, or all requested scrapes are done and you're presenting results.

### Step 0 — 🚀 First-time setup: show the guide first, then verify (Path A only)

> **💡 SKIP RULE**: Step 0 runs only on **Path A** (no prior knowledge, or the user says setup isn't done). If you have prior knowledge the setup is already complete, go **Path B** — Step 0.6 only, no interactive flow. Once `PREFLIGHT_DONE=true` in this session, skip Steps 0/0.6 entirely for later scrapes.

> ⛔ **Rules:**
> 1. **Never** present setup as a "reminder", "note", "things to know", or inline bullet dumps.
> 2. **Never** echo the skill description, pricing, or quota as a lead-in block.
> 3. **Always give a full, clickable URL** — not a `{SITE_URL}` placeholder.
> 4. **Always verify programmatically** — never trust a verbal claim alone.

> 🔒 **Same-browser rule (critical)**: the extension, the MonsterGet login, and the TikTok login must all be in the **same browser**. When guiding, name the browser explicitly: "用 Edge" / "用 Chrome". Never let the user spread the three steps across two browsers.

#### Phase A — Show the full 3-step guide FIRST (before any check)

**A1. Show the complete guide with links** — the user needs to know what to prepare:

> 用这个 skill 前需要准备 3 件事（都用同一个浏览器：**Edge 或 Chrome**）：
> ① 安装 MonsterGet 扩展 → 打开 https://monsterget.com/install 安装
> ② 登录 monsterget.com → 打开 https://monsterget.com 注册并登录
> ③ 登录 TikTok → 打开 https://www.tiktok.com 登录你的账号
>
> 准备好了回复"好了"（或"已装好/已登录"），我会自动检测。

**A2. WAIT** for the user to say they're ready. Do not run checks before this — the user needs the guide first.

**A3. VERIFY everything** — run the silent preflight:
```bash
bash "$SCRIPTS/preflight.sh"
```

- `"ready":true` → all done, jump to **Completion**.
- `"next":"choose_browser"` → **both browsers have the extension and no choice is saved.** Ask the user which to use, run `bash "$SCRIPTS/choose-browser.sh" edge` (or `chrome`), then **re-run `preflight.sh`**. Never guess here — the login checks would run against the wrong browser.
- `"ready":false` otherwise → show the status table, then guide only ❌ items one at a time, starting at `next`.

Show the status with ✅/❌ (naming the browser):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  准备情况检查（浏览器：${BROWSER}）
  ① 安装 MonsterGet 扩展     ✅ 已完成 / ❌ 未安装
  ② 登录 monsterget.com     ✅ 已登录 / ❌ 未登录
  ③ 登录 TikTok             ✅ 已登录 / ❌ 未登录
  提示：3 项都用同一个浏览器（${BROWSER}）操作。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### The per-step protocol (for each unfinished step)

```
for each unfinished step, in order:
  1. TELL    one short message: what to do + the FULL clickable URL + which browser
  2. WAIT    wait for the user to say they're done — never advance early
  3. VERIFY  run THAT step's check script (table below) — programmatically
  4. REPORT  "✅ Step N done" or "❌ Step N failed: <exactly how to fix>"
  5. if ❌   → re-guide → wait → re-verify. Loop until ✅. Do NOT advance.
  → next unfinished step
```

| Step | VERIFY command | Pass condition |
|------|----------------|----------------|
| ① Extension | `bash "$SCRIPTS/detect-browser.sh"` | exit 0, `"extension":true` |
| ② MonsterGet login | `bash "$SCRIPTS/check-login.sh" monsterget` | exit 0, `"logged_in":true` |
| ③ TikTok login | `bash "$SCRIPTS/check-login.sh" tiktok` | exit 0, `"logged_in":true` |

All three ✅ (from pre-check or guidance) → `PREFLIGHT_DONE=true` → tell the user setup is complete → Step 1.

#### Step ① — Install the MonsterGet browser extension

**TELL** — pick the wording based on what Phase A detected:

*If the extension was already detected* (`browser=edge|chrome`):
> **第 1 步 — 扩展已就绪**
> 已检测到 MonsterGet 扩展在 **{BROWSER}** 里，无需重装。
> 后续 2 步都会用 **{BROWSER}**。

*If not detected* (`browser=none`):
> **第 1 步 — 安装 MonsterGet 扩展**
> 打开安装页：**https://monsterget.com/install**
> 把扩展装到 **Edge 或 Chrome**（选一个，后面 3 步都用它）。
> 装好后回复"好了，用 Edge"或"好了，用 Chrome"，我会检测并确认浏览器。

**VERIFY**: re-run `detect-browser.sh` (the extension may have just been installed, so `browser` can change from `none`).

| Result | REPORT | Next |
|--------|--------|------|
| `extension: true` | "✅ 第 1 步完成：扩展已安装在 **{BROWSER}** 里。" | → next unfinished step |
| `extension: false` | "❌ 还没检测到扩展。请确认：① 扩展装好了吗？② 装在了 Edge 还是 Chrome？③ 装完后刷新过 https://monsterget.com/install 吗？装好后回复'好了'。" | re-guide → wait → re-verify |

> 🔁 **After a successful detection, state the browser once more in the next step's message** — so the user never has to remember which browser they picked.

**🚧 Blocking rule**: while ① is `false`, do **not** advance to ② or ③ — both logins must happen in the browser that has the extension.

#### Step ② — Log in to monsterget.com

**TELL** — always name the browser (replace `{BROWSER}` with the actual name):

> **第 2 步 — 登录 monsterget.com（用同一个浏览器：{BROWSER}）**
> 打开：**https://monsterget.com**
> 注册或登录你的账号（游客登录也可以）。
> 完成后回复"好了"，我会自动检测登录状态。

**VERIFY**: `bash "$SCRIPTS/check-login.sh" monsterget` → polls up to 60s (12 × 5s)

| Result | REPORT | Next |
|--------|--------|------|
| `logged_in: true` | "✅ 第 2 步完成：已登录 monsterget.com。" | → next unfinished step |
| `logged_in: false` (timeout) | "❌ 还没有检测到登录。请确认是在刚才安装扩展的同一个浏览器（{BROWSER}）里打开了 https://monsterget.com 并登录，然后回复'好了'。" | re-guide → wait → re-verify |

> A silent browser-launch failure looks exactly like "not logged in" and will send you chasing the wrong problem. The script already retries the launch via the full exe path and reports `browser` in its output — check that field before blaming the user's login.

#### Step ③ — Log in to TikTok

**TELL** — always name the browser (replace `{BROWSER}`):

> **第 3 步 — 登录 TikTok（用同一个浏览器：{BROWSER}）**
> 打开：**https://www.tiktok.com**
> 登录你的 TikTok 账号。
> （如果只抓取非 TikTok 平台，此步可跳过。）
> 完成后回复"好了"，我会自动检测。

**VERIFY**: `bash "$SCRIPTS/check-login.sh" tiktok` → polls up to 60s (12 × 5s)

| Result | REPORT | Next |
|--------|--------|------|
| `logged_in: true` | "✅ 第 3 步完成：已登录 TikTok。" | all three ✅ → setup complete |
| `logged_in: false` (timeout) | "❌ 还没有检测到 TikTok 登录。请确认是在同一个浏览器（{BROWSER}）里登录的，然后回复'好了'。" | re-guide → wait → re-verify |

#### Retry rules (same per-step loop, when a step fails)

1. **Never advance past a failed step.** Only the step that failed is re-checked; steps that already passed are not re-run.
2. **Poll timeout**: 60 seconds max per browser-based check (12 × 5s). Timeout counts as fail.
3. **User wait**: the check script opens the browser and polls immediately — don't interrupt the user. Only speak when reporting ✅/❌.
4. **Blocking**: if ① (extension) is `false`, do not attempt ② or ③.

#### Completion

After all three steps pass, tell the user (in their language) **and offer example prompts** so they know what to say next:

> ✅ 3 项全部通过，可以开始抓取了！
> 试试下面任意一句：
> - 抓取关于 "mike tyson" 的 TikTok 视频 50 条
> - 找出做 "beauty" 内容的 TikTok 创作者 30 个
> - 抓取 #kpop 标签下的视频 30 条
> - 抓取 @tiktok 这位创作者的全部视频
> - 抓取 @mike、@jenifer、@tiktok 的主页数据

(Translate the prompts to the user's language.) Then set `PREFLIGHT_DONE=true` and go to Step 1. Subsequent scrapes in this session skip Steps 0/0.6 entirely.

The check scripts have already written the results to `~/.monsterget/state.json` (including `checked_at`) — no manual write needed.

#### State persistence rules (re-check every conversation)

1. **Every new conversation may read** `~/.monsterget/state.json` for the browser hint and the last check timestamp. This is informational only — it helps you tell the user "上次检查通过于 2026-09-12" and which browser.
2. **Every new conversation re-runs** all checks. The saved results are authority only for the user's visibility, never for skipping verification.
3. **Never skip Phase A** because the state file says everything was OK. `PREFLIGHT_DONE` is always `false` at session start — cold-start contract.
4. The scripts **overwrite** the state file with fresh results and a timestamp on every check.

### Step 0.6 — 🪄 Silent preflight (programmatic, ~20 seconds)

> **Path B entry** — use when you have prior knowledge the setup is already done (memory, a previous session, or the user says "already installed"). **If in doubt about the setup state, run Step 0 (Path A) instead.**

One command does the whole silent preflight — no user interaction, no questions asked:

```bash
bash "$SCRIPTS/preflight.sh"
# → {"ready":false,"next":"extension","extension":true,"platform_reachable":true,
#    "monsterget_login":true,"tiktok_login":true,"browser":"edge","os":"windows"}
```

It runs, in order: `detect-browser.sh` → platform reachability probe → `check-login.sh monsterget` → `check-login.sh tiktok` (short 3×5s probes).

- **Exit 0 (`"ready":true`)** → set `PREFLIGHT_DONE=true`, proceed to Step 1.
- **Exit 1** → read `next` (the first failing step) and escalate to the **interactive Step 0 flow, starting at that step's TELL**. Wait for the user's "done", then re-verify with that single step's script — do not re-run the whole preflight.

| `next` value | Escalate to |
|--------------|-------------|
| `extension` | Step 0 ① |
| `choose_browser` | Ask which browser to use → `choose-browser.sh <edge\|chrome>` → re-run `preflight.sh` |
| `monsterget_login` | Step 0 ② |
| `tiktok_login` | Step 0 ③ |
| `platform_reachable` | Tell the user the platform isn't reachable (network/region). Give them the URL to check. Stop. |

### Step 1 — Platform reachability check

> 💡 If `PREFLIGHT_DONE=true` (set by Step 0 or Step 0.6), this is the **first step** for this scrape — Steps 0/0.6 are skipped.

Quickly probe whether the platform is reachable:

```bash
curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/agent/generate-task-id"
```

- `200` → reachable. Continue.
- Anything else → tell the user the platform isn't reachable yet. For local: ask them to start the backend. Then stop.

### Step 2 — First-time setup (folded into Step 0)

> ✅ The first-time guide was completed in Step 0. Not repeated here.
>
> If the user reports a missing extension or login problem, refer to Step 0's per-step guidance:
> - Install extension: https://monsterget.com/install
> - Log in to MonsterGet: https://monsterget.com
> - Log in to the target site (TikTok): https://www.tiktok.com

### Step 3 — Run a scrape (repeatable)

**One command does the whole thing** — taskId, browser launch, process verification, polling, download:

```bash
bash "$SCRIPTS/run-scrape.sh" <pagePath> <param> <value> [count]
```

#### 3a. Map the user's request to pagePath + param

| User intent | pagePath | param |
|-------------|----------|-------|
| "videos about X" / "search X" | `/tiktok-search-video` | `query=X` |
| "TikTok users/creators doing X" | `/tiktok-search-user` | `query=X` |
| "#tag videos" / "topic X" | `/tiktok-tag` | `query=X` (drop the `#`) |
| "videos by @creator" | `/tiktok-user-videos` | `username=@creator` |
| "profile of @creator" | `/tiktok-profile` | `username=@creator` |

If count isn't given, use the type default (30 for tag/user search, 50 for video/user-videos). Cap at 300. Path segment separator is a **hyphen** (`/tiktok-search-video`), never an underscore.

#### 3b. Run it

```bash
bash "$SCRIPTS/run-scrape.sh" /tiktok-search-video query "mike tyson" 20
# → {"status":"ready","taskId":"...","file":"mike-20-20260905_tiktok_video_ab12cd.csv","rowCount":20,"url":"..."}
```

The script handles, in order:
1. Re-detect the browser (never assumes Edge)
2. Generate a taskId
3. Build the URL (`{SITE_URL}{pagePath}?auto=1&agentTaskId=...&{param}=...&count=N`) — **values are URL-encoded by the script**, so spaces and Chinese characters are safe
4. Open it in the detected browser (fire-and-forget)
5. **Verify the browser process actually started** (up to 3s, then a full-path retry) — a silent launch failure otherwise looks like a task that never appears
6. Poll status every 5s until `ready` / `failed` / `downloaded` / `not_found` (5-minute timeout)
7. Download the CSV with the server's semantic filename into the resolved download dir (see "Where CSVs are saved")

> 🚀 **Do NOT ask the user** "is it open?" after the browser opens. Do not pause, do not read the URL bar. Read the script's JSON output instead — it tells you whether the launch succeeded.

#### 3c. Read the result

| `status` in output | Meaning | What to do |
|--------------------|---------|------------|
| `ready` | CSV downloaded — `file` is the filename, `dir` the folder, `rowCount` the row count | Show the user a preview + the path |
| `not_found` | The page never created the task (launch failed or extension not ready) | Check the `error` field; ask the user to open `url` manually |
| `timeout` | Not ready in 5 min | Extension missing, not logged in, or tab closed — see Troubleshooting |
| `failed` | Task failed on the platform | Report the error |
| `already_downloaded` | The CSV is tombstoned (one download only) | Run again — a new taskId is generated |

#### 3d. Verify & present

Show the user the first rows of the CSV so they can confirm the data is correct. State the saved file path — the scrape output carries it in `dir` (the folder) + `file` (the name).

#### Where CSVs are saved

CSVs go to the **OS default Downloads folder** unless the user picks another location. Resolve order (first match wins):

1. `MONSTERGET_DOWNLOAD_DIR` env var (rarely used)
2. `download_dir` in `~/.monsterget/state.json` (the saved choice)
3. the OS default: `~/Downloads` (Linux uses `xdg-user-dir DOWNLOAD` when available)

**Ask once, before the first scrape of a session** — *"CSV 保存到系统下载目录（`<path>`）可以吗？还是换个路径？"* — then persist the answer:

```bash
bash "$SCRIPTS/set-download-dir.sh"                 # user accepted the default
bash "$SCRIPTS/set-download-dir.sh" "D:/tiktok-data" # user gave a path
# → {"ok":true,"dir":"D:/tiktok-data","source":"custom"}
```

The choice persists across sessions, so ask at most once per machine. Never re-ask if `state.json` already has a `download_dir` unless the user brings it up.

### Step 4 — Bulk creator profiles (optional)

When the user needs profile data for **multiple creators at once** (e.g., "get profiles of @mike, @jenifer, @tiktok"), use the `usernames` param with comma-separated values:

```bash
bash "$SCRIPTS/run-scrape.sh" /tiktok-profile usernames "mike,jenifer,tiktok" 3
```

The platform creates a **parent task** that chains through each profile sequentially. The script polls and downloads exactly as with a single scrape — the CSV contains one row per creator with aggregated profile stats.

### Running multiple scrapes (AI-orchestrated, one at a time)

When the user asks for **several scrapes at once** (e.g. "test all 5 scrapers"), do **not** call them all at once or ask for confirmation between them. Instead, orchestrate them one at a time — the AI is the conductor:

```bash
# Task 1 → wait → result
bash "$SCRIPTS/run-scrape.sh" /tiktok-search-video query "mike tyson" 20
# → show result to the user (CSV path + preview)

# Task 2 → wait → result
bash "$SCRIPTS/run-scrape.sh" /tiktok-search-user query beauty 5
# → show result

# Task 3 → wait → result
bash "$SCRIPTS/run-scrape.sh" /tiktok-tag query kpop 5
# → final summary
```

Key rules:
- **Do not stop to ask the user between tasks.** Each scrape is independent and should run as soon as the previous one is ready. The AI orchestrates, the user watches.
- **The page already inserts a random 5-10s delay** (`auto=1` flow in `_agentAutoStart`) before the scraper window opens. The delay is server-side, so the AI calls `run-scrape.sh` without adding its own sleep.
- **The old browser tab may stay open** — it does not block the next task. Only a task still `pending`/`processing` counts against the concurrency limit.
- **If a scrape returns `429 too_many_concurrent_scrapes`**, a previous task is still `pending`/`processing` — wait for it to be `ready`/`failed`, then retry.
- **Report all results at the end**, together, not one at a time — but show each result's CSV preview as you go so the user trusts progress.
- **Never reimplement a batch loop in the AI** — just chain `run-scrape.sh` calls in sequence. The pacing (5-10s page delay) is built into the page.

## Error handling

| Symptom | Cause | Fix |
|---------|-------|-----|
| `platform_reachable: false` / curl returns nothing | platform not reachable | confirm backend running (local) or site is up (production) |
| `extension: false` | extension not installed / not enabled in that browser | install from https://monsterget.com/install, reload the page |
| `browser did not start` in scrape output | the launch command failed (exe not in PATH) | the script already retries via the full path; if it still fails, ask the user to open `url` manually |
| status `not_found` | the page never created the task — browser never started or extension not ready | verify the browser opened; confirm the extension is installed and enabled |
| status `timeout` (never `ready`, > 5 min) | extension missing, browser not logged in, or tab closed | confirm extension installed + logged in + **page stays open** until the scrape completes |
| page shows "please log in" | not logged in | log in on https://monsterget.com, reopen the page |
| Step ②/③ check times out | browser not logged in (or wrong browser) | log in **in the same browser as the extension**, reply "done", re-check |
| `already_downloaded` | already fetched once | do NOT retry the download; run the scrape again (new taskId) |
| `409 not_ready` | data not ready | keep polling |
| `409 buffer_unavailable` | buffer cleared by TTL race | retry a few seconds later |
| `429 too_many_concurrent_scrapes` | a previous task is still pending/processing | free users have 1 concurrent window — wait for the running task to reach `ready`/`failed`, then retry. Closing the browser tab is NOT required |
| `402 insufficient_credits` | credits exhausted | signup grants 10M credits — almost never runs out; contact the platform |

## Concurrency note

Free-tier users have **1 concurrent scrape window** (plenty for daily use). Member tiers can run **up to 10 in parallel**.

The limit counts **running tasks**, not open windows:
- A task counts while it is `pending` or `processing` (the extension is still working).
- The moment a task reaches `ready`, the slot is **freed** — you can open the next scrape right away.
- **An open browser tab with a finished task does NOT block the next task.** Leave tabs open; there is no need to close them.
- A `pending` task that was never claimed (extension not ready / page abandoned) auto-expires after ~30 seconds.

## Gotchas

- **Use the extension-installed browser.** Never rely on the system default browser — it may not have the extension. `detect-browser.sh` finds it; `run-scrape.sh` uses it.
- **Never call `POST /api/agent/scrape` yourself.** The page does it automatically with the generated taskId. Calling it manually is not needed and requires auth.
- **Never run headless / sandbox scraping.** Scrapes execute in the user's real browser for anti-ban. If you're sandboxed and can't open a local browser (cloud IDE, web-only chat), tell the user to run a local AI terminal (Claude Code CLI, local Codex, Cline, Cursor…).
- **Never re-implement the browser/process/polling logic inline.** The scripts are the single source of truth — that's what makes this work identically across AI clients and operating systems.
- **Keep the tab open** until the task reaches `ready`. Closing the tab before the extension reports results means no server copy is produced.
- **Do not wait for the user between scrapes.** Open → poll → download → next, all in one uninterrupted run.
- After downloading, show the user the CSV path and a preview so they trust the result.
- **Say the account-risk line once per session**, before the first scrape: this drives the user's real TikTok account, and bulk collection may violate TikTok's ToS — the user's account, the user's responsibility. Do not skip this just because the skill says "don't bother the user" — outward-facing actions deserve a confirmation.

## Sources

- Platform: [monsterget.com](https://monsterget.com)
- Skill repository: [github.com/rosstzc/monsterget.com-skills](https://github.com/rosstzc/monsterget.com-skills)

---

## Appendix — zh-CN localized user-facing copy

> Use the Chinese wording below **only** when the user writes to you in Chinese. For all other languages, translate the English text in the body yourself. Never show this appendix to the user.

### Step 0 messages (中文)

> Links must be the **full URL**, never a `{SITE_URL}` placeholder.

**Phase A — 第一步先发完整指引（等用户回复后再检测）**

```
用这个 skill 前需要准备 3 件事（都用同一个浏览器：Edge 或 Chrome）：
① 安装 MonsterGet 扩展 → 打开 https://monsterget.com/install 安装
② 登录 monsterget.com → 打开 https://monsterget.com 注册并登录
③ 登录 TikTok → 打开 https://www.tiktok.com 登录你的账号

准备好了回复"好了"（或"已装好/已登录"），我会自动检测。
```

**Phase B — 用户回复后，显示预检状态表**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  准备情况检查（浏览器：{BROWSER}）
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
