---
name: monsterget-linkedin-collector
description: >-
  Collect LinkedIn data (profiles, similar-profile recommendations, job search,
  people search) through the user's own real browser — anti-blocking, zero-setup,
  permanently free. Requires the free MonsterGet browser extension (one-time
  install), then the AI orchestrates repeatable collections. Supports
  single/batch profile extraction, similar-people recommendations, multi-page
  job search, and people search by keyword/location/industry. Works with Claude
  Code, Codex, Cursor, Windsurf, Cline, ChatGPT.
---

# LinkedIn Collector

> 🎁 **Permanently free · 10 million entries on signup · 1 concurrent window for free users**
> *(Members unlock more parallel windows.)*

## What is this?

A skill that lets **any AI assistant** (Claude Code, WorkBuddy, Codex, Cursor, Windsurf, Cline, ChatGPT…) scrape LinkedIn data — a profile's full detail, the "More profiles for you" recommendation list, job search results, or people search results — and return it as a CSV. No Python packages, no headless configuration, no credential management. The AI orchestrates: it generates a task ID, opens a URL in the **user's own browser**, and downloads the result.

**Why a browser + extension?** The actual scrape runs inside the user's real LinkedIn session (logged in, with the [MonsterGet](https://monsterget.com) browser extension installed). That is what keeps accounts anti-ban safe. There is no server-side LinkedIn scraping — the data is collected right where the user is already logged in.

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
- If the user asks for details, explain what they **can get** (profile info, similar people recommendations, etc.) and how to ask for it — never show how it works under the hood.

## Architecture (what actually happens)

```
AI ──1. GET {BASE_URL}/api/agent/generate-task-id ──▶ {"taskId":"<uuid>"}
AI ──2. open browser page  {pagePath}?auto=1&agentTaskId={taskId}&profileUrl={url}
Page (user browser, logged in + extension) ──▶ auto-fill form + real click on the Start button
                                            ──▶ POST /api/agent/scrape  (creates task with our taskId)
Extension opens the LinkedIn profile page and scrapes it
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
SCRIPTS="$HOME/.monsterget/skills/linkedin-collector/scripts"

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
| `run-scrape.sh <pagePath> <param> <value> [count] [key=value ...]` | Every scrape | End-to-end: taskId → open browser → verify process → poll → download CSV. `more_profiles` should pass `count=50` (see the count rule) |
| `set-download-dir.sh [<dir>]` | First scrape (ask once) | Choose where CSVs are saved. No arg = OS default Downloads dir |

> **🚫 Never run `detect-browser.sh`, `check-login.sh`, or `preflight.sh`** — these are archived reference only. The user guarantees all conditions manually. The AI must not call them during installation, before a scrape, or on failure.

### State file (`~/.monsterget/state.json`)

A small JSON key/value store that persists your browser choice, download directory, and last task info. **Shared with the TikTok skill** — same browser and download directory apply to both platforms:

```json
{"browser_pref":"edge","download_dir":"D:/linkedin-data"}
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

> 要抓取 LinkedIn 数据，需要先在浏览器安装 MonsterGet 扩展。
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

> 请在 **{浏览器}**（装了 MonsterGet 扩展的那个）里完成以下两步：
>
> 1. 打开 **https://monsterget.com** 注册并登录
> 2. 打开 **https://www.linkedin.com** 登录你的 LinkedIn 账号
>
> 都登录好了就可以开始抓取了。我会在每次抓取前提醒你确认条件。

That is it. No detection scripts, no verification loops. The user guarantees the conditions.

> ⚠️ **One-browser rule**: the extension, the [monsterget.com](https://monsterget.com) login, and the LinkedIn login must all be in the **same browser** (the one the user chose). If they later switch browsers, re-run Steps I–III.

## Scrape types — auto-discovered once per session

**Fetch the live scrapers list at session start.** This is the single source of truth — the AI uses it to map the user's request to the correct `pagePath` + `param` + `countMax`. New platforms (LinkedIn scrapers, etc.) are automatically available the moment they are added server-side; no SKILL.md update needed.

```bash
SCRAPERS="$(curl -s "$BASE_URL/api/agent/scrapers")"
```

Each scraper contains all the info needed to build the scrape URL:

| Field | Example | Purpose |
|-------|---------|---------|
| `platform` | `linkedin` | **Filter: this skill only uses `linkedin`** |
| `type` | `linkedin_profile_main` | Stable identifier |
| `name` | `LinkedIn 个人档案` | Human-readable — helps the AI match user intent |
| `page` | `/linkedin-profile-main` | Use as `<pagePath>` in `run-scrape.sh` |
| `param` | `profileUrl` | Use as `<param>` in `run-scrape.sh` |
| `count` / `countMax` | `{min,max,default,scope}` | Count range and scope |
| `usage` | `/linkedin-profile-main?...` | URL template for reference |

**Rules:**
1. `SCRAPERS` is set **once per session** (at the start, before the first scrape). All scrapes in the same session reuse it.
2. **Filter by `platform` first** — this skill only uses `platform: "linkedin"`. If the request is TikTok/X/Upwork, use that platform's skill.
3. To map the user's request, iterate the filtered array by `name` (or `type`) to find the matching entry, then extract `page` + `param`.
4. **⚠️ Count rule (per scraper).**
   - `linkedin_profile_main`: one profile per URL; `count` does not change the row. Omit it, or pass `1`.
   - `linkedin_more_profiles`: the popup renders the full list (usually 20+). Pass **`count=50`** (the platform max) so nothing is truncated. Omitting `count` makes the page default to **30** — that can cut a long list.
   - For batch `profileUrls`, `count` is **per profile**, not the number of profiles. Batch size is the length of the `profileUrls` list.
   - `linkedin_search_jobs`: each page is **25 jobs**; `count` is fixed at `25` (pass `25` or omit it). Use options `page=<start page>` and `pages=<how many pages>`; `pages=0` means **auto-all** (keep paginating until LinkedIn runs out).
   - `linkedin_search_people`: `count` is **per page** (default `10`, max `10`). Use options `page`, `pages` (1–50), and optionally `geo_urn` / `industry` numeric IDs.
5. Profile accepts a full URL (`https://www.linkedin.com/in/username`) or a bare slug (`username`) — the server normalizes.
6. **Batch**: multiple profiles are passed as `profileUrls` (comma-separated) — see "Batch profile pulls" below.
7. **Job search takes a LinkedIn search URL**, not a keyword. Build it in the browser (LinkedIn → Jobs → set keyword/location/filters) and copy the address bar. People search takes a **keyword** plus optional numeric location/industry IDs.

### Current LinkedIn scraper types (reference — the AI fetches live data)

| Type | pagePath | Param | Meaning |
|------|----------|-------|---------|
| `linkedin_profile_main` | `/linkedin-profile-main` | `profileUrl` | Profile header card (name, headline, location, connection, followers, avatar) + full About text, one row per profile |
| `linkedin_more_profiles` | `/linkedin-more-profiles` | `profileUrl` | "More profiles for you" recommendation list (name, headline, connection, avatar, profile URL) for each recommended user |
| `linkedin_search_jobs` | `/linkedin-search-jobs` | `value` (search URL) | Job search results: title, company, location, salary, post time, job URL — 25 per page, multi-page |
| `linkedin_search_people` | `/linkedin-search-people` | `value` (keywords) | People search results: name, headline, location, connection degree, profile URL — multi-page |

## The flow

### 0. Session start — version check + fetch scrapers (once per session)

#### 0a. Version check — auto-update

Run the update script at the **start of the very first task of a session**:

```bash
bash "$SCRIPTS/update-skill.sh"
```

The script outputs JSON. If `updated` is `true`, tell the user the skill was updated and what changed (`changelog`). The output's `scrapers_api` field is informational — the version this skill release was built against; do **not** treat it as the session baseline (that is the last-observed *server* version, read in 0b).

**Read the last-seen scrapers API version** (the baseline for comparison) from the local version file:

```bash
SCRAPERS_API_SEEN="$(sed -n 's/.*"scrapers_api"[[:space:]]*:[[:space:]]*"\([0-9]*\)".*/\1/p' "$HOME/.monsterget/version.json" 2>/dev/null)"
[ -z "$SCRAPERS_API_SEEN" ] && SCRAPERS_API_SEEN="0"
```

If this script or the local version file is missing (old install that predates version tracking), `SCRAPERS_API_SEEN` defaults to `"0"` — the first fetch below will treat the current API version as the baseline and NOT notify.

#### 0b. Fetch the scraper list + version comparison

At the **start of the first task of a session** (after 0a), fetch the live scraper list and compare versions:

```bash
SCRAPERS="$(curl -s "$BASE_URL/api/agent/scrapers")"
```

**Parse `version` from the response** and compare it with the last-seen scrapers API version:

```bash
CURRENT_API_VER="$(printf '%s' "$SCRAPERS" | sed -n 's/.*"version"[[:space:]]*:[[:space:]]*\([0-9]*\).*/\1/p')"
if [ -n "$CURRENT_API_VER" ] && [ "$CURRENT_API_VER" != "$SCRAPERS_API_SEEN" ]; then
  echo "SCRAPER_VERSION_CHANGED=$CURRENT_API_VER (was $SCRAPERS_API_SEEN)"
fi
```

If the version changed (or `SCRAPER_VERSION_CHANGED` is set) **and** `SCRAPERS_API_SEEN` was **not** `"0"` (i.e. this is not the first-ever check), **tell the user in Chinese**:

> 服务器爬虫目录已更新（v{旧版本}→v{新版本}），已新增了一些平台。请确认是否有新的抓取需求。

If this is the **first ever check** (`SCRAPERS_API_SEEN` = `"0"`), treat the current API version as the established baseline — save it and do NOT notify.

**After confirming or notifying**, persist the new version to the local version file so the next session compares against it:

```bash
NEW_API_VER="$(printf '%s' "$SCRAPERS" | sed -n 's/.*"version"[[:space:]]*:[[:space:]]*\([0-9]*\).*/\1/p')"
if [ -n "$NEW_API_VER" ]; then
  LOCAL_VER_FILE="$HOME/.monsterget/version.json"
  mkdir -p "$(dirname "$LOCAL_VER_FILE")"
  [ -f "$LOCAL_VER_FILE" ] || printf '{\n  "skill_version": "0",\n  "extension_version": "unknown",\n  "scrapers_api": "0"\n}\n' > "$LOCAL_VER_FILE"
  # Portable in-place update (no jq dependency) — awk is always present
  awk -v v="$NEW_API_VER" '{ if ($0 ~ /"scrapers_api":/) sub(/"scrapers_api":[[:space:]]*"[^"]*"/, "\"scrapers_api\": \"" v "\""); print }' \
    "$LOCAL_VER_FILE" > "$LOCAL_VER_FILE.tmp" && mv "$LOCAL_VER_FILE.tmp" "$LOCAL_VER_FILE"
  SCRAPERS_API_SEEN="$NEW_API_VER"
fi
```

**If the fetch fails** (platform unreachable), tell the user and stop.

Keep the `SCRAPERS` value and `SCRAPERS_API_SEEN` for the whole session — never re-fetch between tasks in the same conversation.

### 1. Pre-task reminder (every scrape)

At the **start of every scrape task**, before running any command, read the config and print the reminder sentence:

```bash
cat ~/.monsterget/state.json
```

**Say the following block verbatim, translated entirely into the user's language** (never mix languages, never show this English original to the user):

> **I will open {browser} (MonsterGet extension required — install guide: https://monsterget.com/install), visit https://monsterget.com (must be logged in), and scrape https://linkedin.com (must be logged in) for: {user's request}.**
>
> **Important: please shrink the current software window and keep the scraper window partially visible. The browser throttles rendering when the scraper window is fully occluded, which stalls content loading and causes the scrape to fail.**

- Replace `{browser}` with `browser_pref` value ("Edge" or "Chrome"), `{user's request}` with the specific task.
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
# Profile main: one row per profile; omit count or pass 1
bash "$SCRIPTS/run-scrape.sh" /linkedin-profile-main profileUrl "adrienbeaulieu"

# More profiles: pass count=50 to cover the full popup
bash "$SCRIPTS/run-scrape.sh" /linkedin-more-profiles profileUrl "adrienbeaulieu" 50
# → {"status":"ready","taskId":"...","file":"adrienbeaulieu-50-...-monsterget.com.csv","rowCount":23,"empty":false,"url":"..."}

# Job search: paste the LinkedIn search URL, choose page range (or pages=0 for auto-all)
bash "$SCRIPTS/run-scrape.sh" /linkedin-search-jobs value "https://www.linkedin.com/jobs/search-results/?keywords=project%20manager" 25 page=1 pages=3

# People search: keyword + optional numeric location/industry IDs
bash "$SCRIPTS/run-scrape.sh" /linkedin-search-people value "AI engineer" 10 geo_urn=103644278 industry=6 page=1 pages=3
# → {"status":"ready","taskId":"...","file":"AI-engineer-30-...-monsterget.com.csv","rowCount":30,"empty":false,"url":"..."}
```

The script handles, in order:
1. Read the saved browser preference (the user chose during installation)
2. Generate a taskId
3. Build the URL (`{SITE_URL}{pagePath}?auto=1&agentTaskId=...&{param}=...`) — **values are URL-encoded by the script**, so full URLs and Chinese characters are safe
4. Open it in the chosen browser (fire-and-forget)
5. Verify the browser process actually started
6. Poll status every 5s until `ready` / `downloaded` (default 20 min; batch use `MONSTERGET_POLL_TIMEOUT=1800`)
7. Download the CSV with HTTP/file verification

`not_found` is **not terminal** — the page may still be queued behind a 429 concurrency slot.

#### Read the result

| `status` in output | Meaning | What to do |
|--------------------|---------|------------|
| `ready` | CSV downloaded — `file`, `dir`, `rowCount`, `empty` | Show a preview + the path |
| `ready` + `empty:true` | Task completed with 0 rows | Check LinkedIn login / private profile |
| `not_found` | The page never created the task (launch failed, extension not ready, or still queued) | Ask the user to check the 3 conditions (see Step 3) |
| `timeout` | Not ready within the configured window | See Step 3 — checklist |
| `already_downloaded` | The CSV is tombstoned (one download only) | Run again — a new taskId is generated |

#### Verify & present

Show the user the first rows of the CSV so they can confirm the data is correct. State the saved file path — the scrape output carries it in `dir` (the folder) + `file` (the name).

#### Where CSVs are saved

CSVs go to the **OS default Downloads folder** unless the user picks another location. Resolve order (first match wins):

1. `MONSTERGET_DOWNLOAD_DIR` env var (rarely used)
2. `download_dir` in `~/.monsterget/state.json` (the saved choice)
3. the OS default: `~/Downloads` (Linux uses `xdg-user-dir DOWNLOAD` when available)

**Ask once, before the first scrape of a session** — *"CSV 保存到系统下载目录（`<path>`）可以吗？还是换个路径？"* — then persist the answer:

```bash
bash "$SCRIPTS/set-download-dir.sh"                 # user accepted the default
bash "$SCRIPTS/set-download-dir.sh" "D:/linkedin-data" # user gave a path
# → {"ok":true,"dir":"D:/linkedin-data","source":"custom"}
```

The choice persists across sessions, so ask at most once per machine. Never re-ask if `state.json` already has a `download_dir`.

### 3. On failure — user checklist

If the scrape fails (status `not_found`, `timeout`, or the browser never opened), **do not re-run the script** — instead, prompt the user to check the three conditions:

> 抓取失败了，请确认以下 3 项（都在 **{browser}** 里）：
>
> ① **安装了 MonsterGet 扩展吗？**
>    → 打开 https://monsterget.com/install 安装
>
> ② **在安装了扩展的那个浏览器登录了 [monsterget.com](https://monsterget.com) 吗？**
>    → 打开 https://monsterget.com 登录
>
> ③ **在同一个浏览器登录了 [linkedin.com](https://www.linkedin.com) 且能正常访问吗？**
>    → 打开 https://www.linkedin.com 确认
>
> 全部确认后告诉我"好了"，我重新抓取。

Wait for the user to respond, then retry the scrape from Step 2.

### Batch profile pulls (optional)

When the user needs profile data for **multiple LinkedIn profiles at once** (e.g., "get the profiles of adrienbeaulieu, satyanadella, tvdong"), use the `profileUrls` param with comma-separated values:

```bash
bash "$SCRIPTS/run-scrape.sh" /linkedin-profile-main profileUrls "adrienbeaulieu,satyanadella,tvdong"
```

The platform creates a **parent task** that chains through each profile sequentially. The script polls and downloads exactly as with a single scrape — the CSV contains one row per profile with aggregated profile stats.

Same for recommendations (each profile's full recommendation list):

```bash
bash "$SCRIPTS/run-scrape.sh" /linkedin-more-profiles profileUrls "adrienbeaulieu,satyanadella"
```

> **Note**: with `run-scrape.sh`, the `profileUrls` values must be comma-separated on one line. Full URLs and bare slugs both work. `count` is **per profile**; for `linkedin_more_profiles` pass `50`, for `linkedin_profile_main` omit it or pass `1`.

### Job search (multi-page)

The user usually describes the job search in natural language ("remote product manager jobs posted this week"). Two ways to get the URL:

1. **User already has a search URL** — use it verbatim (it keeps every filter: keyword, location, salary, date posted, remote, …).
2. **Build a basic URL** from the keywords:
   `https://www.linkedin.com/jobs/search-results/?keywords=<url-encoded keywords>`
   For richer filters, ask the user to open LinkedIn Jobs, set the filters, and paste the address bar. Do not invent filter parameters.

```bash
# Pages 1-3 (75 jobs)
bash "$SCRIPTS/run-scrape.sh" /linkedin-search-jobs value "https://www.linkedin.com/jobs/search-results/?keywords=data%20analyst" 25 page=1 pages=3

# Auto-all pages (keep going until no more results — set a longer poll window)
MONSTERGET_POLL_TIMEOUT=3600 bash "$SCRIPTS/run-scrape.sh" /linkedin-search-jobs value "https://www.linkedin.com/jobs/search-results/?keywords=data%20analyst" 25 pages=0
```

- `page` is the **starting** page (1-based); `pages` is how many pages to collect. `pages=0` = auto-all.
- Each page is 25 jobs; `rowCount` ≈ 25 × pages collected.
- The platform creates one parent task and chains the pages automatically — one CSV at the end.

### People search (multi-page)

People search uses a keyword plus optional **numeric** LinkedIn IDs:

- `geo_urn` — location ID (e.g. `103644278` = United States, `102890883` = Greater China)
- `industry` — industry ID (e.g. `6` = Technology, `43` = Finance, `14` = Healthcare, `4` = Education)

How to get an ID: run the search on linkedin.com, look at the address bar, and copy the number inside `geoUrn=["..."]` or `industry=["..."]`. If the user does not care about a filter, omit that option.

```bash
# 3 pages × 10 results
bash "$SCRIPTS/run-scrape.sh" /linkedin-search-people value "AI engineer" 10 geo_urn=103644278 industry=6 page=1 pages=3
```

- `count` is per page (10 by default, max 10 — use `pages` for more rows).
- Total rows ≈ `count × pages` (LinkedIn may return fewer on the last page).

### Running multiple scrapes (AI-orchestrated, one at a time)

When the user asks for **several scrapes at once**, orchestrate them one at a time — the AI is the conductor:

```bash
# Task 1 → wait → result
bash "$SCRIPTS/run-scrape.sh" /linkedin-profile-main profileUrl "adrienbeaulieu"
# → show result to the user (CSV path + preview)

# Task 2 → wait → result
bash "$SCRIPTS/run-scrape.sh" /linkedin-more-profiles profileUrl "satyanadella"
# → show result

# Task 3 → wait → result
bash "$SCRIPTS/run-scrape.sh" /linkedin-profile-main profileUrls "tvdong,min-gao-358161141"
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
| `not_found` / `timeout` | Extension missing, not logged in, or browser launch failed | Run the 3-point user checklist (Step 3) |
| `platform_reachable: false` / curl returns nothing | Platform not reachable | Confirm backend running (local) or site is up (production) |
| page shows "please log in" | Not logged into [monsterget.com](https://monsterget.com) | Log in at [monsterget.com](https://monsterget.com), retry |
| `already_downloaded` | Already fetched once | Run the scrape again (new taskId) |
| `409 not_ready` | Data not ready yet | Keep polling |
| `409 buffer_unavailable` | Buffer cleared by TTL race | Retry a few seconds later |
| `429 too_many_concurrent_scrapes` | A previous task is still pending/processing | Free users have 1 concurrent window — the page self-retries ~5 min; keep polling. Closing the browser tab is NOT required |
| `402 insufficient_credits` | Credits exhausted | Signup grants 10M credits — almost never runs out; contact the platform |
| CSV has empty `name` / `about` for a profile | LinkedIn needs login, or the profile is private | Ask the user to confirm they are logged into LinkedIn (Step 3 ③) |

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
- After downloading, show the user the CSV path and a preview so they trust the result.
- **Say the account-risk line once per batch**, before the first scrape: this drives the user's real LinkedIn account, and bulk collection may violate LinkedIn's ToS — the user's account, the user's responsibility.
- **The pre-task reminder (Step 1) exists because the user opted out of auto-detection.** It is the user's only signal that the browser is about to open. Never skip it.
- **Never run `detect-browser.sh`, `check-login.sh`, or `preflight.sh`.** They exist in the scripts directory but are deliberately unused — the AI must never call them.
- **LinkedIn profile scraping needs the user logged into LinkedIn** in the extension browser — the extension opens the profile page in that session. If the scrape returns empty fields, the most common cause is the user not being logged in.

## Sources

- Platform: [monsterget.com](https://monsterget.com)
- Skill repository: [github.com/monsterget-com/skills](https://github.com/monsterget-com/skills)
