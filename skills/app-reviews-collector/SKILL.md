---
name: monsterget-app-reviews-collector
description: >-
  Collect public App Store (iOS) and Google Play (Android) app reviews through
  the user's own browser — no API key, no proxies, permanently free. Requires
  the free MonsterGet browser extension (one-time install), then the AI
  orchestrates repeatable review collections and returns CSV. Supports
  multi-country App Store reviews, multi-language Google Play reviews, star
  filters, date filters, and developer replies. Works with Claude Code, Codex,
  Cursor, Windsurf, Cline, ChatGPT.
---

# App Reviews Collector

> 🎁 **Permanently free · 10 million entries on signup · 1 concurrent window for free users**
> *(Members unlock more parallel windows.)*

## What is this?

A skill that lets **any AI assistant** (Claude Code, WorkBuddy, Codex, Cursor, Windsurf, Cline, ChatGPT…) collect public app-store reviews — **iOS App Store** and **Android Google Play** — and return them as a CSV. No Python packages, no headless configuration, no credential management. The AI orchestrates: it generates a task ID, opens a URL in the **user's own browser**, and downloads the result.

**Why a browser + extension?** The data is fetched inside the user's real browser by the [MonsterGet](https://monsterget.com) extension. There is no server-side scraping, no proxy pool, and no app-store account needed — reviews are public.

## 🌍 Language rule (read before anything else)

**Always communicate with the user in the user's own language.** Every message you print for the user — setup guidance, progress updates, failure explanations, the final result summary — must be in the language the user writes to you in. This skill's instructions are written in English for precision, but that is *not* the language you speak to the user.

- User writes Chinese → reply in Chinese
- User writes Japanese → reply in Japanese
- User writes Spanish / Portuguese / Korean / … → reply in that language
- Never mix two languages in one user-facing message

## ⚠️ How to answer "how to use" questions (read first)

> **The user is never shown the implementation details in this file** — only the end result.

When the user asks "怎么使用", "how to use", or anything asking for usage guidance:
- **Never show bash commands, script paths, API endpoints, taskIds, polling, state file paths, or any internals** in your answer.
- Keep your answer conversational and short (4–8 lines), with 2-3 example natural-language prompts.
- Implementation details like `run-scrape.sh`, `pagePath`, `BASE_URL`, `STATE_FILE`, `SCRIPTS=` are for *your execution only* — the user never needs to see them.
- If the user asks for details, explain what they **can get** (App Store / Google Play reviews, ratings, countries/languages, developer replies, etc.) and how to ask for it — never show how it works under the hood.

## Architecture (what actually happens)

```
AI ──1. GET {BASE_URL}/api/agent/generate-task-id ──▶ {"taskId":"<uuid>"}
AI ──2. open browser page  {pagePath}?auto=1&agentTaskId={taskId}&value={app}&count=N&countries=...
Page (user browser, logged in + extension) ──▶ auto-fill form + real click on the Start button
                                            ──▶ POST /api/agent/scrape  (creates task with our taskId)
Extension fetches the public review API inside the app-store page
Page relays rows to server buffer
AI ──3. GET {BASE_URL}/api/agent/delivery/task/{taskId}/status  ──▶ {status:"ready"}
AI ──4. GET {BASE_URL}/api/agent/delivery/task/{taskId}/data    ──▶ CSV download
```

**Key invariant:** the AI generates the taskId itself *before* opening the browser, so it never needs to read the browser address bar.

**Human-like trigger:** the auto-start branch types into the visible form and dispatches real mouse events on the page's Start button. The page's own submit flow then runs — only its task-creation request is routed to `/api/agent/scrape`, so the task is still an agent task with CSV delivery. Manual clicking is unchanged.

## Configuration

```text
BASE_URL   = https://monsterget.com      # API host (usually same as SITE_URL)
SITE_URL   = https://monsterget.com      # page host
STATE_FILE = ~/.monsterget/state.json    # persisted settings (browser choice, download dir, …)
```

Override via environment variables: `MONSTERGET_BASE_URL=http://localhost:8000` (and optionally `MONSTERGET_SITE_URL`, `MONSTERGET_STATE_DIR`).

**Link rule**: the user-facing links below are written for production (`https://monsterget.com/install`, `https://monsterget.com`). If the platform runs locally, substitute the domain with the configured `SITE_URL` — never show a bare `{SITE_URL}` placeholder to the user. Always produce a full, clickable URL.

## 🧩 Scripts — the runtime

**Resolve the scripts directory once, at the start of the session, and reuse it:**

```bash
SCRIPTS="$HOME/.monsterget/skills/app-reviews-collector/scripts"

if [ ! -d "$SCRIPTS" ]; then
  echo "Skill not installed: run the install instruction first." >&2
  echo "SCRIPTS=$SCRIPTS" >&2
  exit 1
fi
echo "SCRIPTS=$SCRIPTS"
```

Every command below is written as `bash "$SCRIPTS/<name>.sh"`.

### Scripts used in this flow

| Script | When | What it does |
|--------|------|--------------|
| `update-skill.sh` | Session start — auto-update check | Compares local skill version against GitHub, auto-downloads updates. Also outputs `scrapers_api` for version tracking |
| `choose-browser.sh <edge\|chrome>` | Installation — user picks a browser | Saves the browser preference (`browser_pref`) to state |
| `run-scrape.sh <pagePath> <param> <value> [count] [key=value ...]` | Every scrape | End-to-end: taskId → open browser → verify process → poll → download CSV. Extra `key=value` args carry countries/languages/stars/sort/delay |
| `set-download-dir.sh [<dir>]` | First scrape (ask once) | Choose where CSVs are saved. No arg = OS default Downloads dir |

> **🚫 Never run `detect-browser.sh`, `check-login.sh`, or `preflight.sh`** — these are archived reference only (they are not shipped in this skill). The user guarantees all conditions manually.

### State file (`~/.monsterget/state.json`)

A small JSON key/value store that persists your browser choice, download directory, and last task info. **Shared with the other MonsterGet skills** — same browser and download directory apply to every platform:

```json
{"browser_pref":"edge","download_dir":"D:/reviews-data"}
```

- **`browser_pref`** — the browser the user chose during installation (`edge` or `chrome`). Set by `choose-browser.sh`. Read it at the start of every task to produce the reminder sentence.
- **`download_dir`** — where CSVs are saved. Set by `set-download-dir.sh`.
- Read the file with: `cat ~/.monsterget/state.json`.

## Installation Guide (one-time, ~2 minutes)

> This skill does **no automatic detection** — every condition is verified manually. The AI only reminds, never checks.
>
> Complete the three steps below once, and every subsequent session is ready to scrape.

### Step I — Install the MonsterGet extension

Tell the user (in their language, with full clickable links):

> 要抓取应用商店评论，需要先在浏览器安装 MonsterGet 扩展。
>
> 安装页：**https://monsterget.com/install**
>
> 可以安装在 **Chrome** 或 **Edge**。
>
> 装好后告诉我装在了哪个浏览器（回复"Edge"或"Chrome"）。

**Wait for the user to reply** — do not proceed until they confirm which browser.

### Step II — Save the browser choice

The user replied with "Edge" or "Chrome". Save it:

```bash
bash "$SCRIPTS/choose-browser.sh" edge
# → {"ok":true,"browser_pref":"edge"}
```

(Use `chrome` if that is what the user chose.)

### Step III — Tell the user to log in

Tell the user (naming the browser they chose):

> 请在 **{浏览器}**（装了 MonsterGet 扩展的那个）里打开 **https://monsterget.com** 注册并登录。
>
> 不需要登录 App Store 或 Google Play —— 评论是公开数据，扩展会直接采集。

That is it. No detection scripts, no verification loops. The user guarantees the conditions.

> ⚠️ **One-browser rule**: the extension and the [monsterget.com](https://monsterget.com) login must be in the **same browser** (the one the user chose). If they later switch browsers, re-run Steps I–III.

## Scrape types — auto-discovered once per session

**Fetch the live scrapers list at session start.** This is the single source of truth — the AI uses it to map the user's request to the correct `pagePath` + `param` + `countMax`.

```bash
SCRAPERS="$(curl -s "$BASE_URL/api/agent/scrapers")"
```

Each scraper contains all the info needed to build the scrape URL:

| Field | Example | Purpose |
|-------|---------|---------|
| `platform` | `app_store` | **Filter: this skill uses `app_store` and `google_play`** |
| `type` | `app_store_reviews` | Stable identifier |
| `name` | `App Store 评论` | Human-readable — helps the AI match user intent |
| `page` | `/app-store-reviews` | Use as `<pagePath>` in `run-scrape.sh` |
| `param` | `value` | Use as `<param>` in `run-scrape.sh` |
| `input` | `{kind, batch, maxBatch}` | `url` — a product URL or an app id/package |
| `count` | `{min,max,default,scope}` | Count range; scope is **per country / per language** |
| `options` | `{countries, stars, sort, ...}` | Extra `key=value` args for `run-scrape.sh` |
| `usage` | `/app-store-reviews?...` | URL template for reference |

**Rules:**
1. `SCRAPERS` is set **once per session** (at the start, before the first scrape). All scrapes in the same session reuse it.
2. **Filter by `platform` first** — this skill only uses `platform: "app_store"` or `platform: "google_play"`. If the request is TikTok/X/LinkedIn/Upwork, use that platform's skill.
3. To map the user's request, iterate the filtered array by `name` (or `type`) to find the matching entry, then extract `page` + `param` + `count`.
4. `<param>` is always `value`; extra options go after `<count>` as `key=value`.
5. The app input accepts a **full product URL** or the **id/package**:
   - App Store: `https://apps.apple.com/cn/app/id741292507` or `741292507`
   - Google Play: `https://play.google.com/store/apps/details?id=com.xingin.xhs` or `com.xingin.xhs`

### Current app-review scraper types (reference — the AI fetches live data)

| Type | pagePath | Param | Count | Options |
|------|----------|-------|-------|---------|
| `app_store_reviews` | `/app-store-reviews` | `value` (App URL/ID) | per country, default 500, max 10000 | `countries`, `stars`, `since`, `sort`, `text_only`, `include_replies`, `delay_ms` |
| `google_play_reviews` | `/google-play-reviews` | `value` (URL/package) | per language, default 500, max 5000 | `languages`, `stars`, `sort`, `text_only`, `include_replies`, `delay_ms` |

**Count is per country / per language, not the total.** `countries=cn,jp` + `count=500` means up to 1000 reviews (500 per country). Same for `languages=zh-CN,en` + `count=500` → up to 1000.

## The flow

### 0. Session start — version check + fetch scrapers (once per session)

#### 0a. Version check — auto-update

Run the update script at the **start of the very first task of a session**:

```bash
bash "$SCRIPTS/update-skill.sh"
```

The script outputs JSON. If `updated` is `true`, tell the user the skill was updated and what changed (`changelog`).

**Read the last-seen scrapers API version** from the shared version file:

```bash
SCRAPERS_API_SEEN="$(sed -n 's/.*"scrapers_api"[[:space:]]*:[[:space:]]*"\([0-9]*\)".*/\1/p' "$HOME/.monsterget/version.json" 2>/dev/null)"
[ -z "$SCRAPERS_API_SEEN" ] && SCRAPERS_API_SEEN="0"
```

#### 0b. Fetch the scraper list + version comparison

```bash
SCRAPERS="$(curl -s "$BASE_URL/api/agent/scrapers")"
```

Parse `version` and compare with the last-seen value. If it changed **and** `SCRAPERS_API_SEEN` was not `"0"`, tell the user in their language:

> 服务器爬虫目录已更新（v{旧版本}→v{新版本}），新增了一些爬虫。请确认是否有新的抓取需求。

Then persist the new version with the same portable `awk` snippet used by the other skills (update only the `scrapers_api` field in `~/.monsterget/version.json`). Keep `SCRAPERS` and `SCRAPERS_API_SEEN` for the whole session — never re-fetch between tasks in the same conversation.

**If the fetch fails** (platform unreachable), tell the user and stop.

### 1. Pre-task reminder (every scrape)

At the **start of every scrape task**, before running any command, read the config and print the reminder sentence:

```bash
cat ~/.monsterget/state.json
```

**Say the following block verbatim, translated entirely into the user's language** (never mix languages, never show this English original to the user):

> **I will open {browser} (MonsterGet extension required — install guide: https://monsterget.com/install), visit https://monsterget.com (must be logged in), and collect public reviews from {apps.apple.com or play.google.com} for: {user's request}. No app-store login is needed.**
>
> **Important: please shrink the current software window and keep the scraper window partially visible. The browser throttles rendering when the scraper window is fully occluded, which stalls content loading and causes the scrape to fail.**

- Replace `{browser}` with `browser_pref` value ("Edge" or "Chrome"), `{user's request}` with the specific app/task, and the store host with the one being scraped.
- **The entire block is one message.** Translate it as a whole — every line, including the install guide URL — into the user's language. Do not split, reorder, or omit any part.
- **This reminder is mandatory on every single scrape.** It is the user's only confirmation that the AI is about to open their browser. Do not skip it, shorten it, or merge it into a "processing…" status line.

**Never run `run-scrape.sh` until the reminder has been printed.** Proceed to Step 2 without waiting for a reply — the reminder is informational, not a question.

### 2. Run the scrape

**One command does the whole thing** — taskId, browser launch, process verification, polling, download:

```bash
bash "$SCRIPTS/run-scrape.sh" <pagePath> <param> <value> [count] [key=value ...]
```

Examples:

```bash
# App Store: one country, newest reviews
bash "$SCRIPTS/run-scrape.sh" /app-store-reviews value "https://apps.apple.com/cn/app/id741292507" 500 countries=cn

# App Store: two countries, 1-2 star reviews, date cutoff
bash "$SCRIPTS/run-scrape.sh" /app-store-reviews value "https://apps.apple.com/us/app/id284882215" 200 countries=us,gb stars=1,2 since=2026-01-01

# Google Play: two languages, 5-star only, most helpful first
bash "$SCRIPTS/run-scrape.sh" /google-play-reviews value "com.xingin.xhs" 300 languages=zh-CN,en stars=5 sort=helpful
# → {"status":"ready","taskId":"...","file":"com.xingin.xhs-300-...-monsterget.com.csv","rowCount":287,"empty":false,"url":"..."}
```

The script handles, in order:
1. Read the saved browser preference (the user chose during installation)
2. Generate a taskId
3. Build the URL (`{SITE_URL}{pagePath}?auto=1&agentTaskId=...&value=...&count=N&options...`) — **values are URL-encoded by the script**, so URLs and Chinese characters are safe
4. Open it in the chosen browser (fire-and-forget)
5. Verify the browser process actually started
6. Poll status every 5s until `ready` / `downloaded` (default 20-minute timeout; large multi-country runs can set `MONSTERGET_POLL_TIMEOUT=3600`)
7. Download the CSV with the server's semantic filename; check HTTP 200/409/410 and file non-empty

`not_found` is **not terminal** — the page may still be queued behind a 429 concurrency slot (the page self-retries for up to ~5 minutes).

#### Read the result

| `status` in output | Meaning | What to do |
|--------------------|---------|------------|
| `ready` | CSV downloaded — `file`, `dir`, `rowCount`, `empty` | Show a preview + the path |
| `ready` + `empty:true` | Task completed with 0 rows | The app may have no reviews in that country/language, or the filters are too narrow |
| `not_found` | The page never created the task (launch failed, extension not ready, or still queued) | Ask the user to check the conditions (see Step 3) |
| `timeout` | Not ready within the configured window | See Step 3 — checklist; for big multi-country runs raise the poll window |
| `already_downloaded` | The CSV is tombstoned (one download only) | Run again — a new taskId is generated |

#### Verify & present

Show the user the first rows of the CSV so they can confirm the data is correct. State the saved file path — the scrape output carries it in `dir` (the folder) + `file` (the name).

Columns are localized to the page language, matching the platform UI:

- App Store: `平台, 评论ID, 评分, 标题, 正文, 用户, 时间, 国家, 已编辑, 开发者回复`
- Google Play: `平台, 评论ID, 评分, 正文, 用户, 时间, 语言, 点赞数, 版本, 开发者回复, 回复时间`

#### Where CSVs are saved

CSVs go to the **OS default Downloads folder** unless the user picks another location. Resolve order (first match wins):

1. `MONSTERGET_DOWNLOAD_DIR` env var (rarely used)
2. `download_dir` in `~/.monsterget/state.json` (the saved choice)
3. the OS default: `~/Downloads` (Linux uses `xdg-user-dir DOWNLOAD` when available)

**Ask once, before the first scrape of a session** — *"CSV 保存到系统下载目录（`<path>`）可以吗？还是换个路径？"* — then persist the answer:

```bash
bash "$SCRIPTS/set-download-dir.sh"                    # user accepted the default
bash "$SCRIPTS/set-download-dir.sh" "D:/reviews-data"  # user gave a path
# → {"ok":true,"dir":"D:/reviews-data","source":"custom"}
```

The choice persists across sessions, so ask at most once per machine. Never re-ask if `state.json` already has a `download_dir`.

### 3. On failure — user checklist

If the scrape fails (status `not_found`, `timeout`, or the browser never opened), **do not re-run the script** — instead, prompt the user to check the conditions:

> 抓取失败了，请确认以下 2 项（都在 **{browser}** 里）：
>
> ① **安装了 MonsterGet 扩展吗？**
>    → 打开 https://monsterget.com/install 安装
>
> ② **在安装了扩展的那个浏览器登录了 [monsterget.com](https://monsterget.com) 吗？**
>    → 打开 https://monsterget.com 登录
>
> 另外请确认能正常打开 **{apps.apple.com / play.google.com}**。全部确认后告诉我"好了"，我重新抓取。

Wait for the user to respond, then retry the scrape from Step 2.

### Options reference

| Option | Type | Default | Meaning |
|--------|------|---------|---------|
| `countries` | comma list | country from the App Store URL, else `us` | App Store country storefronts, max 10 (e.g. `cn,jp,us`) |
| `languages` | comma list | `zh-CN,en` | Google Play review languages, max 10 (e.g. `en,zh-CN,ja`) |
| `stars` | comma list | all | Star filter `1..5` (e.g. `1,2` = negative reviews) |
| `since` | `YYYY-MM-DD` | empty | App Store only — stop at this date (works with `sort=recent`) |
| `sort` | enum | App Store `recent`, Google Play `newest` | App Store: `recent`/`helpful`; Google Play: `newest`/`helpful` |
| `text_only` | `0`/`1` | `1` | Keep only reviews that contain text |
| `include_replies` | `0`/`1` | `1` | Keep developer replies |
| `delay_ms` | int | `600` | Delay between review API requests (200–3000); raise it for very large runs |
| `rss_fallback` | `0`/`1` | `1` | App Store only — fall back to the public RSS feed if the review API is empty |

### Running multiple scrapes (AI-orchestrated, one at a time)

When the user asks for **several apps at once**, orchestrate them one at a time — the AI is the conductor:

```bash
# Task 1 → wait → result
bash "$SCRIPTS/run-scrape.sh" /app-store-reviews value "https://apps.apple.com/us/app/id284882215" 500 countries=us
# → show result to the user (CSV path + preview)

# Task 2 → wait → result
bash "$SCRIPTS/run-scrape.sh" /google-play-reviews value "com.xingin.xhs" 500 languages=zh-CN,en
# → show result

# Task 3 → wait → result
bash "$SCRIPTS/run-scrape.sh" /app-store-reviews value "https://apps.apple.com/jp/app/id333903271" 300 countries=jp
# → final summary
```

Key rules:
- **Do not stop to ask the user between tasks.** Each scrape is independent and should run as soon as the previous one is ready.
- **The pre-task reminder is said once at the start of the batch**, not repeated per task within the batch. Say: *"我将连续抓取以下内容……"* then chain the scrapes.
- **The page already inserts a random 3–6s anti-detection delay** before the scraper window opens — the AI should not add its own sleep.
- **If a scrape returns `429 too_many_concurrent_scrapes`**, the page automatically waits and retries for up to ~5 minutes. Do not create duplicate tasks; keep polling.

## Error handling

| Symptom | Cause | Fix |
|---------|-------|-----|
| `not_found` / `timeout` | Extension missing, not logged into monsterget.com, or browser launch failed | Run the user checklist (Step 3) |
| `platform_reachable: false` / curl returns nothing | Platform not reachable | Confirm backend running (local) or site is up (production) |
| page shows "please log in" | Not logged into [monsterget.com](https://monsterget.com) | Log in at [monsterget.com](https://monsterget.com), retry |
| `already_downloaded` | Already fetched once | Run the scrape again (new taskId) |
| `409 not_ready` | Data not ready yet | Keep polling |
| `409 buffer_unavailable` | Buffer cleared by TTL race | Retry a few seconds later |
| `429 too_many_concurrent_scrapes` | A previous task is still pending/processing | Free users have 1 concurrent window — the page self-retries ~5 min; keep polling. Closing the browser tab is NOT required |
| `402 insufficient_credits` | Credits exhausted | Signup grants 10M credits — almost never runs out; contact the platform |
| `ready` + `empty:true` | Task completed with 0 rows | App may have no reviews in that storefront/language, or the star/date filters are too narrow |
| Only a few hundred rows for a huge app | The store API caps how far back it paginates | Try more countries/languages, or a smaller `since` window |

## Concurrency note

Free-tier users have **1 concurrent scrape window**. Member tiers can run **up to 10 in parallel**.

The limit counts **running tasks**, not open windows:
- A task counts while it is `pending` or `processing` (the extension is still working).
- The moment a task reaches `ready`, the slot is **freed** — you can open the next scrape right away.
- An open browser tab with a finished task does **NOT** block the next task.
- A `pending` task that was never claimed auto-expires after ~30 seconds.

## Gotchas

- **Use the extension-installed browser.** Never rely on the system default browser — it may not have the extension. The user chose which browser during installation; that browser must have the extension installed.
- **Never re-implement the browser/process/polling logic inline.** The scripts are the single source of truth — that is what makes this work identically across AI clients and operating systems.
- **Keep the tab open until the task reaches `ready`.** The extension normally closes the scraper window and task page automatically 45–90 seconds after completion; do not close them manually before `ready`.
- **No app-store login is required** — reviews are public. If the user asks to log into the App Store/Google Play, tell them it is not necessary.
- **Count is per country / per language.** Do the multiplication for the user when they ask "how many will I get".
- After downloading, show the user the CSV path and a preview so they trust the result.
- **The pre-task reminder (Step 1) exists because the user opted out of auto-detection.** It is the user's only signal that the browser is about to open. Never skip it.

## Sources

- Platform: [monsterget.com](https://monsterget.com)
- Skill repository: [github.com/monsterget-com/skills](https://github.com/monsterget-com/skills)
