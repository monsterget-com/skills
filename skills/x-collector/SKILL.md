---
name: monsterget-x-collector
description: >-
  Collect X/Twitter data (search feeds, user search, profiles, user tweets,
  tweet details, tweet comments, home feed) through the user's own real browser
  — anti-blocking, zero-setup, permanently free. Requires the free MonsterGet
  browser extension (one-time install), then the AI orchestrates repeatable
  collections. Works with Claude Code, Codex, Cursor, Windsurf, Cline, ChatGPT.
---

# X / Twitter Collector

> 🎁 **Permanently free · 10 million entries on signup · 1 concurrent window for free users**
> *(Members unlock more parallel windows.)*

## What is this?

A skill that lets **any AI assistant** collect X/Twitter data — keyword search,
user search, account profiles, a user's tweets, tweet details, tweet comments,
or the home feed — and return it as a CSV. No Python packages, no headless
configuration, no credential management. The AI orchestrates: it generates a
task ID, opens a URL in the **user's own browser**, and downloads the result.

**Why a browser + extension?** The actual scrape runs inside the user's real X
session (logged in, with the [MonsterGet](https://monsterget.com) browser
extension installed). There is no server-side X scraping.

## 🌍 Language rule (read before anything else)

**Always communicate with the user in the user's own language.** Every message
you print for the user — setup guidance, progress updates, failure explanations,
the final result summary — must be in the language the user writes to you in.

- User writes Chinese → reply in Chinese
- User writes Japanese → reply in Japanese
- User writes Spanish / Portuguese / Korean / … → reply in that language
- Never mix two languages in one user-facing message

The zh-CN localized wording for user-facing messages is in the **Appendix** at
the end of this file.

## ⚠️ How to answer "how to use" questions

When the user asks "怎么使用", "how to use", or anything asking for usage guidance:

- **Never show bash commands, script paths, API endpoints, taskIds, polling,
  state file paths, or any internals** in your answer.
- Keep the answer conversational and short (4–8 lines), with 2-3 example
  natural-language prompts.
- Implementation details like `run-scrape.sh`, `pagePath`, `BASE_URL`,
  `STATE_FILE`, `SCRIPTS=` are for *your execution only*.

## Architecture (what actually happens)

```
AI ──1. GET {BASE_URL}/api/agent/generate-task-id ──▶ {"taskId":"<uuid>"}
AI ──2. open browser page  {pagePath}?auto=1&agentTaskId={taskId}&value=...&count=N
Page (user browser, logged in + extension) ──▶ auto-fill form + real click on the Start button
                                            ──▶ POST /api/agent/scrape
Extension executes scrape in X tab
AI ──3. GET {BASE_URL}/api/agent/delivery/task/{taskId}/status ──▶ {status:"ready"}
AI ──4. GET {BASE_URL}/api/agent/delivery/task/{taskId}/data    ──▶ CSV download
```

The page auto-start branch is isolated behind `auto=1&agentTaskId`; manual X
scraping flow is untouched. In auto-start, the page types into the visible form
and dispatches real mouse events on the Start button; only the task-creation
call is routed to `/api/agent/scrape`, so the task stays an agent task.

## Configuration

```text
BASE_URL   = https://monsterget.com      # API host (usually same as SITE_URL)
SITE_URL   = https://monsterget.com      # page host
STATE_FILE = ~/.monsterget/state.json    # persisted browser choice / download dir
```

Override via environment variables: `MONSTERGET_BASE_URL=http://localhost:8000`
(and optionally `MONSTERGET_SITE_URL`, `MONSTERGET_STATE_DIR`).

**Link rule**: user-facing links use the production domain. If the platform runs
locally, substitute the configured `SITE_URL` — never show a bare `{SITE_URL}`.

## 🧩 Scripts — the runtime

Resolve the scripts directory once per session:

```bash
SCRIPTS="$HOME/.monsterget/skills/x-collector/scripts"
[ -d "$SCRIPTS" ] || { echo "Skill not installed: run the install instruction first." >&2; exit 1; }
```

Scripts:

| Script | When | What it does |
|--------|------|--------------|
| `update-skill.sh` | Session start | Compare local version with GitHub, auto-update |
| `choose-browser.sh <edge\|chrome>` | Installation | Save the browser preference |
| `run-scrape.sh <pagePath> <param> <value> [count] [key=value ...]` | Every scrape | taskId → open browser → poll → download CSV |
| `set-download-dir.sh [<dir>]` | First scrape | Choose where CSVs are saved |

> **🚫 Never run `detect-browser.sh`, `check-login.sh`, or `preflight.sh`** — archived reference only.

## Installation Guide (one-time, ~2 minutes)

This skill does **no automatic detection** — the user confirms manually.

### Step I — Install the MonsterGet extension

Tell the user (in their language, with full clickable links):

> 要抓取 X/Twitter 数据，需要先在浏览器安装 MonsterGet 扩展。
>
> 安装页：**https://monsterget.com/install**
>
> 可以安装在 **Chrome** 或 **Edge**。
>
> 装好后告诉我装在了哪个浏览器（回复"Edge"或"Chrome"）。

**Wait for the user to reply** — do not proceed until they confirm the browser.

### Step II — Save the browser choice

```bash
bash "$SCRIPTS/choose-browser.sh" edge
# → {"ok":true,"browser_pref":"edge"}
```

(Use `chrome` if that is what the user chose.)

### Step III — Tell the user to log in

> 请在 **{浏览器}**（装了 MonsterGet 扩展的那个）里完成以下两步：
>
> 1. 打开 **https://monsterget.com** 注册并登录
> 2. 打开 **https://x.com** 登录你的 X 账号
>
> 都登录好了就可以开始抓取了。

> ⚠️ **One-browser rule**: extension, monsterget.com login, and X login must all
> be in the same browser.

## Scrape types — auto-discovered once per session

Fetch the live catalog at the start of the first task:

```bash
SCRAPERS="$(curl -s "$BASE_URL/api/agent/scrapers")"
```

This skill only uses entries whose `platform` is `x`. Ignore TikTok/LinkedIn/Upwork
entries. Each X entry carries `type`, `page`, `input`, `count`, `options`, `usage`.

| User intent | pagePath | param | value | Common options |
|---|---|---|---|---|
| Search posts about X | `/x-search-timeline` | `value` | keyword | `sort=top\|latest` |
| Find X users | `/x-search-user` | `value` | keyword | — |
| Profile of @user | `/x-user-profile` | `value` / `values` | `@user` or profile URL | batch via comma list |
| Tweets by @user | `/x-user-videos-api` | `value` | `@user` | — |
| Details of a tweet | `/x-tweet-detail` | `value` / `values` | tweet URL or ID | `export_video`, `export_images`, `export_cover` |
| Comments of a tweet | `/x-tweet-comments` | `value` / `values` | tweet URL or ID | `comment_sort=relevance\|recent\|likes`, `include_spam=0\|1` |
| Home feed | `/x-home-timeline` | `-` | empty | `feed=for_you\|following` |

**Count semantics**

- Most types: `count` = number of rows to collect.
- `x_user_profile` and `x_tweet_detail`: `count` is **per item** and fixed at 1.
- `x_tweet_comments`: `count` = comments per tweet (1–1000, default 200).
- Batch types: pass `values` as a **comma-separated list**; `count` still applies
  per item. Max batch: profile 50, tweet detail 20, tweet comments 10.

## The flow

### 0. Session start — version check + fetch catalog (once per session)

```bash
bash "$SCRIPTS/update-skill.sh"
SCRAPERS="$(curl -s "$BASE_URL/api/agent/scrapers")"
```

If the script reports `updated: true`, tell the user what changed. If the fetch
fails, tell the user and stop.

### 1. Pre-task reminder (every scrape)

Read `~/.monsterget/state.json` and print the reminder in the user's language:

> **I will open {browser} (MonsterGet extension required — install guide:
> https://monsterget.com/install), visit https://monsterget.com (must be logged
> in), and scrape https://x.com (must be logged in) for: {user's request}.**
>
> **Important: please shrink the current software window and keep the scraper
> window partially visible. The browser throttles rendering when the scraper
> window is fully occluded.**

Never run `run-scrape.sh` until this reminder has been printed. Proceed without
waiting for a reply.

### 2. Run the scrape

```bash
bash "$SCRIPTS/run-scrape.sh" <pagePath> <param> <value> [count] [key=value ...]
```

Examples:

```bash
# Search posts, newest first
bash "$SCRIPTS/run-scrape.sh" /x-search-timeline value "ai tool" 50 sort=latest

# User search
bash "$SCRIPTS/run-scrape.sh" /x-search-user value "growth hacker" 30

# Profile (single)
bash "$SCRIPTS/run-scrape.sh" /x-user-profile value "@satyanadella" 1

# Profiles (batch)
bash "$SCRIPTS/run-scrape.sh" /x-user-profile values "@satyanadella,@elonmusk" 1

# User tweets
bash "$SCRIPTS/run-scrape.sh" /x-user-videos-api value "@satyanadella" 50

# Tweet detail (batch)
bash "$SCRIPTS/run-scrape.sh" /x-tweet-detail values "https://x.com/a/status/111,https://x.com/b/status/222" 1

# Tweet comments
bash "$SCRIPTS/run-scrape.sh" /x-tweet-comments value "https://x.com/a/status/111" 200 comment_sort=recent include_spam=0

# Home feed
bash "$SCRIPTS/run-scrape.sh" /x-home-timeline - "" 50 feed=following
```

Batch runs can take longer than 5 minutes. Set a larger timeout when needed:

```bash
MONSTERGET_POLL_TIMEOUT=1800 bash "$SCRIPTS/run-scrape.sh" /x-tweet-comments values "url1,url2" 200
```

The script handles: taskId → URL encode → open browser → verify process → poll
(default 20 min) → download CSV with HTTP/file verification. It never asks the
user anything.

#### Read the result

| `status` | Meaning | Action |
|----------|---------|--------|
| `ready` | CSV downloaded — `file`, `dir`, `rowCount`, `empty` | Show preview + path |
| `ready` + `empty:true` | Task completed with 0 rows | Tell the user no data was returned |
| `not_found` | Page never created the task (not loaded / extension not ready / still queued) | Run the 3-point checklist |
| `timeout` | Not ready within the poll window | Run the 3-point checklist |
| `already_downloaded` | CSV tombstoned | Run again (new taskId) |

#### Where CSVs are saved

1. `MONSTERGET_DOWNLOAD_DIR` env var
2. `download_dir` in `~/.monsterget/state.json`
3. OS default `~/Downloads`

Ask once per machine, then persist:

```bash
bash "$SCRIPTS/set-download-dir.sh"                 # default
bash "$SCRIPTS/set-download-dir.sh" "D:/x-data"     # custom
```

### 3. On failure — user checklist

If the scrape fails (`not_found`, `timeout`, browser never opened), do not
blindly re-run. Ask the user to check, in the chosen browser:

> 抓取失败了，请确认以下 3 项（都在 **{浏览器}** 里）：
>
> ① **安装了 MonsterGet 扩展吗？**
>    → 打开 https://monsterget.com/install 安装
>
> ② **登录了 monsterget.com 吗？**
>    → 打开 https://monsterget.com 登录
>
> ③ **登录了 x.com 且能正常访问吗？**
>    → 打开 https://x.com 确认
>
> 全部确认后告诉我"好了"，我重新抓取。

## Error handling

| Symptom | Cause | Fix |
|---------|-------|-----|
| `not_found` / `timeout` | Extension missing, not logged in, page closed, or still queued | 3-point checklist |
| `platform_reachable: false` / curl empty | Platform unreachable | Confirm site/backend is up |
| `already_downloaded` | CSV already fetched | Run again (new taskId) |
| `409 not_ready` | Data not ready | Keep polling |
| `409 buffer_unavailable` | Buffer TTL race | Script retries; if still failing, run again |
| `429 too_many_concurrent_scrapes` | Previous task still pending/processing | Page auto-retries ~5 min; wait, then retry |
| `402 insufficient_credits` | Credits exhausted | Signup grants 10M; contact platform |
| Empty CSV / `empty:true` | No matching posts/comments, or X requires login | Confirm X login; try a broader query |

## Concurrency note

Free-tier users have **1 concurrent scrape window**. Member tiers can run more
(up to 10). The limit counts **running tasks**, not open windows. The moment a
task reaches `ready`, the slot is freed. The extension closes the scraper window
and task page automatically after completion (45–90s); do not close it before
the task is ready.

## Gotchas

- **Use the extension-installed browser.** Never rely on the system default.
- **Never re-implement browser/process/polling logic inline.** The scripts are
  the single source of truth.
- **X login is required** for search, profiles, tweets, comments, and home feed.
  If fields are empty, the most common cause is not being logged in.
- **Batch comments are heavier**: each tweet opens its own detail page; keep the
  batch small (≤10) and expect longer runtimes.
- **The page auto-start branch is additive**: manual X scraping still uses the
  original page buttons and APIs.

## Sources

- Platform: [monsterget.com](https://monsterget.com)
- Skill repository: [github.com/monsterget-com/skills](https://github.com/monsterget-com/skills)

---

## Appendix — zh-CN localized user-facing copy

### Installation checklist

```
要抓取 X/Twitter 数据，需要先在浏览器安装 MonsterGet 扩展。

安装页：https://monsterget.com/install

可以安装在 Chrome 或 Edge。

装好后告诉我装在了哪个浏览器（回复"Edge"或"Chrome"）。
```

```
请在 {浏览器}（装了 MonsterGet 扩展的那个）里完成以下两步：

1. 打开 https://monsterget.com 注册并登录
2. 打开 https://x.com 登录你的 X 账号

都登录好了就可以开始抓取了。
```

### Failure checklist

```
抓取失败了，请确认以下 3 项（都在 {浏览器} 里）：

① 安装了 MonsterGet 扩展吗？
   → 打开 https://monsterget.com/install 安装

② 登录了 monsterget.com 吗？
   → 打开 https://monsterget.com 登录

③ 登录了 x.com 且能正常访问吗？
   → 打开 https://x.com 确认

全部确认后告诉我"好了"，我重新抓取。
```
