---
name: tiktok-scraper
description: 🎁 Permanently free — 10M entries on signup, 1 concurrent window. Zero-install skill: open a browser URL, the extension + logged-in session do the rest. TikTok video search, creator discovery, hashtag collection, user video export to CSV. Works with Claude Code, Codex, Cursor, Windsurf, ChatGPT (any AI client). No Python packages, no credentials, no headless setup.
---

# TikTok Scraper

> 🎁 **永久免费 · 注册即享 1000万条额度 · 免费用户 1 个并发窗口**
> *(Permanently free · 10 million entries on signup · 1 concurrent window for free users. Members unlock more parallel windows.)*

## What is this?

A skill that lets **any AI assistant** (Claude Code, Codex, Cursor, Windsurf, ChatGPT…) scrape TikTok data — video search, creator discovery, hashtag collection, or a specific creator's videos — and return it as a CSV. You don't install Python packages, configure headless browsers, or manage credentials. The AI orchestrates: it generates a task ID, opens a URL in the **user's own browser**, and downloads the result.

**Why a browser + extension?** The actual scrape runs inside the user's real TikTok session (logged in, with the [MonsterGet](https://monsterget.com) browser extension installed). That's what keeps the accounts anti-ban safe. There is no server-side TikTok scraping — the data is collected right where the user is already logged in.

**First-time setup (one-time, ~2 minutes):** the user registers a free account at [monsterget.com](https://monsterget.com) and installs the extension (Chrome/Edge). Everything after that is repeatable and instant.

Scrape TikTok data through the MonsterGet platform running on the user's machine — **zero install, zero credentials, zero Python packages for the user**. The scrape runs in the **user's real browser** with an installed extension and logged-in session (anti-ban core). The AI just orchestrates.

## When to use

User wants TikTok data: video search, user/creator search, hashtag/tag search, or a specific creator's videos — typically for market research, competitor analysis, influencer discovery, content monitoring.

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
DEFAULT_BROWSER = msedge                     # msedge | chrome | open (mac) | xdg-open (linux)
```

Change `SITE_URL`/`BASE_URL` when the platform is running locally (`http://localhost:8000`).

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

Follow these steps in order. Steps 0–2 are one-time setup; steps 3–4 are repeated per scrape.

### ⚡ Automation contract (read this first)

**Opening the browser is fire-and-forget. Never pause to ask the user "is it open?" or "shall I continue?"**

Once you run the browser-open command, the page executes on its own — it creates the task with the taskId you already hold and the extension runs it. Your job is to *immediately* start polling. There is nothing to wait for.

Rules that make the AI fast instead of slow:

1. **Open + poll in one shot.** Run the browser-open command and the poll loop together (see Step 3c). Do not put a message to the user between them.
2. **Never wait for user confirmation** after opening the browser. The user does not need to do anything (unless they aren't logged in yet — that's the one exception, and it shows up as the scrape never reaching `ready`).
3. **Polling already detects completion.** The poll loop exits the moment the status is `ready` (or `failed`). You do not need to ask the user whether the task finished — the status endpoint tells you.
4. **Multiple scrapes run back-to-back, unattended.** When the user asks for several scrapes, run them in a loop: open → poll → download → open the next one. Do **not** stop and report back between tasks. See "Running multiple scrapes" below.
5. **A finished task frees the concurrency slot.** The scrape window may stay open — it does not block the next task. Only a task still `pending`/`processing` counts against the limit.
6. **Only speak to the user** when: you need a one-time setup step (Step 0/2), a scrape fails, or all requested scrapes are done and you're presenting results.

### Step 0 — Confirm the environment (first time only)

Before anything, confirm with the user:
- The platform backend is running (production `monsterget.com` is always on; for local, user must start `localhost:8000`).
- **Which browser has the MonsterGet extension installed?** Chrome or Edge? Remember it for the session.

### Step 1 — Preflight check (first time or when scraping fails)

Quickly probe whether the platform is reachable and whether the extension handshake works:

```bash
# Reachability
curl -s -o /dev/null -w "%{http_code}" {BASE_URL}/api/agent/generate-task-id
```

- `200` → reachable. Continue.
- Anything else → tell the user the platform isn't reachable yet. For local: ask them to start the backend. Then stop.

If scraping previously failed with an extension error, ask the user to verify the extension is installed and the browser is logged in (see Troubleshooting).

### Step 2 — Register / install extension (only if not already done)

The scrape must run in a browser that is **logged in to {SITE_URL} and has the extension installed**. AI cannot do this itself — guide the user:

| Need | Action |
|------|--------|
| No account | Ask user to open `{SITE_URL}`, register and log in (guest login also supported) |
| No extension | Ask user to open `{SITE_URL}/install` and follow install prompts (Chrome/Edge both supported) |
| Not sure | Ask the user to confirm both are done before continuing |

Wait for explicit user confirmation after each.

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

```bash
# Edge (Windows) — or substitute chrome / open / xdg-open per Step 0 choice
start msedge "https://monsterget.com/tiktok-search-video?auto=1&agentTaskId=$TASK_ID&query=mike&count=10"
```

If `start` isn't available, use the full exe path:
```bash
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" "https://monsterget.com/tiktok-search-video?auto=1&agentTaskId=$TASK_ID&query=mike&count=10"
```

> 🚀 **Do NOT wait after opening the browser.** The command returning means the browser process was launched — that's all you need. Do not ask the user "is it open?", do not pause, do not read the URL bar. The page creates the task with the taskId you already hold and runs automatically. **Go straight to Step 3d and poll.**

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
start msedge "https://monsterget.com/tiktok-profile?auto=1&agentTaskId=$TASK_ID&usernames=mike,jenifer,tiktok&count=3"
```

The platform creates a **parent task** that chains through each profile sequentially. Poll and download using `$TASK_ID` — the CSV contains one row per creator with aggregated profile stats.

### Running multiple scrapes (serial batch)

When the user asks for **several scrapes at once** (e.g. "test all 5 scrapers"), run them **back-to-back in a loop, unattended**:

```
1. TASK_ID = generate-task-id
2. open browser page 1          (fire-and-forget)
3. poll until ready             (background)
4. download CSV 1
5. TASK_ID = generate-task-id
6. open browser page 2          ← do NOT wait for the user between tasks
7. poll → download
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
| status endpoint → `404 delivery_not_found` | wrong taskId | re-run 3a and regenerate |
| status stays `processing` > 5 min | extension missing, browser not logged in, or page closed | confirm extension installed + logged in + page still open; page must stay open until scrape completes |
| status endpoint never reaches `ready`, page shows "extension not ready" | extension not installed / not enabled | install extension from `{SITE_URL}/install`, reload page |
| page shows "please log in" | not logged in | log in on `{SITE_URL}`, reopen page |
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
