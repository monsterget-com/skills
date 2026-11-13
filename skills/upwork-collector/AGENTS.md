# Upwork Jobs Collector (MonsterGet)

Collect Upwork job search results as CSV, driven by an AI agent, scraped
through the user's real logged-in browser via the MonsterGet extension
(anti-ban). Works in any AI client that can run shell commands.

## Language rule

Always reply to the user in the user's own language (zh → 中文, ja → 日本語, es → Español, …).

## ⚠️ Answering "how to use" questions

Never show bash commands, script paths, API endpoints, taskIds, polling logic,
state files, or implementation details. Reply in 4-8 conversational lines with
2-3 example prompts:

> 你可以直接对我这样说：
>
> - "找一下 Upwork 上关于 **Amazon** 的岗位 20 条"
> - "抓取这个 Upwork 搜索链接的第一页：https://www.upwork.com/nx/search/jobs?q=..."
>
> 我会自动帮你抓取并生成 CSV 文件。

## When to use

The user asks for Upwork jobs: roles matching a keyword, a specific Upwork
search URL, a number of pages, or "all jobs" for a query.

## How it works

```
AI builds an Upwork search URL ──▶ opens browser page with auto=1&agentTaskId
──▶ page creates parent + page sub-tasks ──▶ extension scrapes each page
──▶ AI polls delivery status ──▶ downloads CSV
```

No server-side Upwork scraping. The scrape runs inside the user's real Upwork
session.

## First-run flow (pure manual — no code verification)

The user needs 3 things, all in the **same browser**:

a. Show the guide in the user's language:

> 用这个 skill 前需要准备 3 件事（都用同一个浏览器：**Edge 或 Chrome**）：
> ① 安装 MonsterGet 扩展 → 打开 https://monsterget.com/install 安装
> ② 登录 monsterget.com → 打开 https://monsterget.com 注册并登录
> ③ 登录 Upwork → 打开 https://www.upwork.com 登录你的账号
>
> 装好扩展后告诉我装在了哪个浏览器（回复"Edge"或"Chrome"），全部准备好了回复"好了"。

b. **WAIT**. Never run detection scripts or scan the disk.

c. Save the browser choice:

```bash
bash ~/.monsterget/skills/upwork-collector/scripts/choose-browser.sh edge
# (or chrome)
```

d. Confirm + offer examples:

> ✅ 都准备好了，可以开始抓取了！
> 试试下面任意一句：
> - 找一下 Upwork 上关于 "Amazon" 的岗位 10 条
> - 抓取这个 Upwork 搜索链接的前 3 页：https://www.upwork.com/nx/search/jobs?q=python

## Scripts

```bash
SCRIPTS="$HOME/.monsterget/skills/upwork-collector/scripts"
[ -d "$SCRIPTS" ] || { echo "Skill not installed — run the install instruction first." >&2; exit 1; }
```

| Script | Purpose |
|--------|---------|
| `update-skill.sh` | Session start — auto-update check |
| `choose-browser.sh <edge\|chrome>` | Save browser choice |
| `run-scrape.sh <pagePath> <param> <value> [count] [key=value ...]` | Full scrape → CSV |
| `set-download-dir.sh [<dir>]` | Choose CSV folder |

> **🚫 Never run `detect-browser.sh`, `check-login.sh`, or `preflight.sh`.**

### Scrape

```bash
bash "$SCRIPTS/run-scrape.sh" /upwork-search-jobs value "<searchUrl>" <per_page> page=1 pages=1
```

| Option | Meaning |
|--------|---------|
| `value` | Full Upwork search URL (`https://www.upwork.com/nx/search/jobs?...`) |
| `count` | `per_page` from the URL (10 or 50) |
| `page` | Start page (default 1) |
| `pages` | 1–100, or `0` = auto-all |

Examples:

```bash
bash "$SCRIPTS/run-scrape.sh" /upwork-search-jobs value \
  "https://www.upwork.com/nx/search/jobs?q=amazon&per_page=10" 10 page=1 pages=1

MONSTERGET_POLL_TIMEOUT=1800 bash "$SCRIPTS/run-scrape.sh" /upwork-search-jobs value \
  "https://www.upwork.com/nx/search/jobs?q=python&per_page=10" 10 page=1 pages=3
```

Output:

```json
{"status":"ready","taskId":"...","file":"...csv","dir":"...","rowCount":20,"empty":false,"url":"..."}
```

## Behavior rules for the agent

- Build a valid Upwork search URL from the user's request (`q=` keyword,
  optional filters, `per_page=10` or `50`).
- **Default to 1 page.** Only use `pages=0` when the user explicitly asks for
  all jobs; it can run long.
- **Open + verify + poll in one shot.** Never ask "is the browser open?".
- **Show the CSV path + a few rows.**
- **First scrape each session**: tell the user once that this drives their real
  Upwork account; the user is responsible for complying with Upwork's terms.
- **Pre-task reminder**: before every scrape, read `~/.monsterget/state.json`
  and say the reminder from SKILL.md.

## Common errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `not_found` / `timeout` | Extension missing, not logged in, or tab closed | 3-point manual checklist |
| `invalid_param` | Not an upwork.com search URL | Ask for a valid search URL |
| `already_downloaded` | CSV already fetched | Run again (new taskId) |
| `429 too_many_concurrent_scrapes` | Free tier has 1 slot | Wait; page auto-retries |
| `empty:true` | No matching jobs | Broaden query / check filters |
