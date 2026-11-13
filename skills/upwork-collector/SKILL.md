---
name: monsterget-upwork-collector
description: >-
  Collect Upwork job search results through the user's own real browser —
  anti-blocking, zero-setup, permanently free. Requires the free MonsterGet
  browser extension (one-time install), then the AI orchestrates repeatable
  job collections and returns CSV. Works with Claude Code, Codex, Cursor,
  Windsurf, Cline, ChatGPT.
---

# Upwork Jobs Collector

> 🎁 **Permanently free · 10 million entries on signup · 1 concurrent window for free users**
> *(Members unlock more parallel windows.)*

## What is this?

A skill that lets **any AI assistant** collect Upwork job search results and
return them as a CSV. The AI orchestrates: it generates a task ID, builds an
Upwork search URL from the user's request, opens it in the **user's own
browser**, and downloads the result.

**Why a browser + extension?** The scrape runs inside the user's real Upwork
session (logged in, with the [MonsterGet](https://monsterget.com) browser
extension installed). There is no server-side Upwork scraping.

## 🌍 Language rule

**Always communicate with the user in the user's own language.** Every message
you print for the user — setup, progress, failure explanations, the final result
summary — must be in the user's language.

## ⚠️ How to answer "how to use" questions

When the user asks "怎么使用", "how to use", or similar:

- Never show bash commands, script paths, API endpoints, taskIds, polling, state
  files, or any internals.
- Reply conversationally (4–8 lines) with 2-3 example prompts:

> 你可以直接对我这样说：
>
> - "找一下 Upwork 上关于 **Amazon** 的岗位 20 条"
> - "抓取这个 Upwork 搜索链接的第一页：https://www.upwork.com/nx/search/jobs?q=..."
>
> 我会自动帮你抓取并生成 CSV 文件。

## Architecture

```
AI ──1. GET {BASE_URL}/api/agent/generate-task-id ──▶ {"taskId":"<uuid>"}
AI ──2. open {pagePath}?auto=1&agentTaskId={taskId}&value={searchUrl}&count=10&page=1&pages=1
Page ──▶ auto-fill form + real click on the Start button → POST /api/agent/scrape  (creates parent + page sub-tasks)
Extension opens the first Upwork search page; autoNext chains the rest
AI ──3. poll /api/agent/delivery/task/{taskId}/status
AI ──4. download CSV
```

The auto-start branch types into the visible form and dispatches real mouse
events on the Start button; only the task-creation call is routed to
`/api/agent/scrape`, so the task stays an agent task. Manual clicking is
unchanged.

## Configuration

```text
BASE_URL   = https://monsterget.com
SITE_URL   = https://monsterget.com
STATE_FILE = ~/.monsterget/state.json
```

Override with `MONSTERGET_BASE_URL=http://localhost:8000`, `MONSTERGET_SITE_URL`,
`MONSTERGET_STATE_DIR`.

## 🧩 Scripts

```bash
SCRIPTS="$HOME/.monsterget/skills/upwork-collector/scripts"
[ -d "$SCRIPTS" ] || { echo "Skill not installed: run the install instruction first." >&2; exit 1; }
```

| Script | When | What it does |
|--------|------|--------------|
| `update-skill.sh` | Session start | Auto-update check |
| `choose-browser.sh <edge\|chrome>` | Installation | Save browser preference |
| `run-scrape.sh <pagePath> <param> <value> [count] [key=value ...]` | Every scrape | taskId → open → poll → CSV |
| `set-download-dir.sh [<dir>]` | First scrape | Choose CSV folder |

> **🚫 Never run `detect-browser.sh`, `check-login.sh`, or `preflight.sh`.**

## Installation Guide (one-time)

### Step I — Install the MonsterGet extension

> 要抓取 Upwork 数据，需要先在浏览器安装 MonsterGet 扩展。
>
> 安装页：**https://monsterget.com/install**
>
> 可以安装在 **Chrome** 或 **Edge**。
>
> 装好后告诉我装在了哪个浏览器（回复"Edge"或"Chrome"）。

Wait for the user's reply.

### Step II — Save the browser choice

```bash
bash "$SCRIPTS/choose-browser.sh" edge   # or chrome
```

### Step III — Tell the user to log in

> 请在 **{浏览器}**（装了 MonsterGet 扩展的那个）里完成以下两步：
>
> 1. 打开 **https://monsterget.com** 注册并登录
> 2. 打开 **https://www.upwork.com** 登录你的 Upwork 账号
>
> 都登录好了就可以开始抓取了。

> ⚠️ Extension, monsterget.com login, and Upwork login must be in the same
> browser.

## Scrape type

Fetch the live catalog once per session:

```bash
SCRAPERS="$(curl -s "$BASE_URL/api/agent/scrapers")"
```

Use only the entry with `platform: "upwork"`:

| Type | pagePath | param | value | Options |
|------|----------|-------|-------|---------|
| Upwork jobs | `/upwork-search-jobs` | `value` | full Upwork search URL | `page` (start page), `pages` (0 = auto-all, 1–100) |

**Building the search URL**

Upwork search URLs look like:

```text
https://www.upwork.com/nx/search/jobs?q=amazon&per_page=10
https://www.upwork.com/nx/search/jobs?q=python&contractor_tier=1&per_page=50
```

- `q` = keyword(s)
- `per_page` = 10 or 50 (the collector uses this as `count`)
- You may pass any Upwork search filters the user asks for.

**Pages**

- `pages=1` (default): one page.
- `pages=N` (1–100): N pages, chained by the extension.
- `pages=0`: auto-all — keep fetching until a page is not full. Use only when
  the user explicitly asks for "all jobs" / "as many as possible".

## The flow

### 0. Session start

```bash
bash "$SCRIPTS/update-skill.sh"
SCRAPERS="$(curl -s "$BASE_URL/api/agent/scrapers")"
```

### 1. Pre-task reminder (every scrape)

Read `~/.monsterget/state.json` and print in the user's language:

> **I will open {browser} (MonsterGet extension required — install guide:
> https://monsterget.com/install), visit https://monsterget.com (must be logged
> in), and scrape https://www.upwork.com (must be logged in) for: {user's request}.**
>
> **Important: please shrink the current software window and keep the scraper
> window partially visible.**

### 2. Run the scrape

```bash
bash "$SCRIPTS/run-scrape.sh" /upwork-search-jobs value "<searchUrl>" <per_page> page=1 pages=1
```

Examples:

```bash
# One page, 10 jobs
bash "$SCRIPTS/run-scrape.sh" /upwork-search-jobs value \
  "https://www.upwork.com/nx/search/jobs?q=amazon&per_page=10" 10 page=1 pages=1

# Three pages
MONSTERGET_POLL_TIMEOUT=1800 bash "$SCRIPTS/run-scrape.sh" /upwork-search-jobs value \
  "https://www.upwork.com/nx/search/jobs?q=python&per_page=10" 10 page=1 pages=3

# Auto-all (use only when the user asks for all)
MONSTERGET_POLL_TIMEOUT=1800 bash "$SCRIPTS/run-scrape.sh" /upwork-search-jobs value \
  "https://www.upwork.com/nx/search/jobs?q=designer&per_page=10" 10 page=1 pages=0
```

The script handles taskId, URL encoding, browser launch, polling (default
20 min), and CSV download with HTTP/file verification.

Output:

```json
{"status":"ready","taskId":"...","file":"...csv","dir":"...","rowCount":20,"empty":false,"url":"..."}
```

### 3. On failure — user checklist

> 抓取失败了，请确认以下 3 项（都在 **{浏览器}** 里）：
>
> ① 安装了 MonsterGet 扩展吗？→ https://monsterget.com/install
> ② 登录了 monsterget.com 吗？→ https://monsterget.com
> ③ 登录了 upwork.com 且能正常访问吗？→ https://www.upwork.com
>
> 全部确认后告诉我"好了"，我重新抓取。

## Error handling

| Symptom | Cause | Fix |
|---------|-------|-----|
| `not_found` / `timeout` | Extension missing, not logged in, page closed, or queued | 3-point checklist |
| `platform_reachable: false` | Platform unreachable | Confirm site/backend |
| `invalid_param` (platform) | URL is not an upwork.com search link | Ask the user for a valid Upwork search URL |
| `already_downloaded` | CSV tombstoned | Run again |
| `429 too_many_concurrent_scrapes` | Previous task still running | Wait; page auto-retries |
| `empty:true` | No jobs matched the URL | Broaden the query / check filters |

## Gotchas

- **Upwork login is required.** If the page shows a login wall, no jobs are
  returned.
- **Page URL must be an Upwork search page**, not a job detail page.
- **`pages=0` can run a long time.** Prefer `pages=1` or a specific page count.
- **The page auto-start branch is additive.** Manual Upwork scraping on the
  site is unchanged.

## Sources

- Platform: [monsterget.com](https://monsterget.com)
- Skill repository: [github.com/monsterget-com/skills](https://github.com/monsterget-com/skills)
