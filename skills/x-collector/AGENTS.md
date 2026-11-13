# X / Twitter Collector (MonsterGet)

Collect X/Twitter data — search feeds, user search, profiles, user tweets,
tweet details, tweet comments, and home feed — as CSV, driven by an AI agent,
scraped through the user's real logged-in browser via the MonsterGet extension
(anti-ban). Works in any AI client that can run shell commands.

## Language rule

Always reply to the user in the user's own language (zh → 中文, ja → 日本語, es → Español, …).

## ⚠️ Answering "how to use" questions

When the user asks "怎么使用", "how to use", or anything equivalent:

**Never show bash commands, script paths (`run-scrape.sh`, `choose-browser.sh`),
API endpoints (`monsterget.com/api/…`), taskIds, polling logic, VERSION.json,
state.json, or any implementation detail.**

Reply with 4-8 lines of conversational text in the user's language, giving 2-3
example natural-language prompts:

> 你可以直接对我这样说：
>
> - "搜索 X 上关于 **ai tool** 的推文 50 条"
> - "抓取 **@satyanadella** 的账号资料"
> - "抓取这条推文的评论：https://x.com/..."
>
> 我会自动帮你抓取并生成 CSV 文件。

## When to use

The user asks for X/Twitter data: posts about a keyword, users matching a
keyword, a profile's stats, a user's tweets, a tweet's details, a tweet's
comments, or their home feed.

## How it works

```
AI generates taskId ──▶ opens browser URL ──▶ page creates task, extension scrapes ──▶ AI polls status ──▶ AI downloads CSV
```

No server-side X scraping. The scrape runs inside the user's real X session
(logged in, with the MonsterGet extension).

## First-run flow (pure manual — no code verification)

The user needs 3 things, all in the **same browser**:

a. Show the full 3-step guide with links (in the user's language):

> 用这个 skill 前需要准备 3 件事（都用同一个浏览器：**Edge 或 Chrome**）：
> ① 安装 MonsterGet 扩展 → 打开 https://monsterget.com/install 安装
> ② 登录 monsterget.com → 打开 https://monsterget.com 注册并登录
> ③ 登录 X → 打开 https://x.com 登录你的账号
>
> 装好扩展后告诉我装在了哪个浏览器（回复"Edge"或"Chrome"），全部准备好了回复"好了"。

b. **WAIT** for the user to reply. **Never run any detection script, never scan
the disk, never verify programmatically.** The user's manual confirmation is the
only check.

c. Save the browser choice:

```bash
bash ~/.monsterget/skills/x-collector/scripts/choose-browser.sh edge
# (or chrome)
```

d. Confirm + offer example prompts:

> ✅ 都准备好了，可以开始抓取了！
> 试试下面任意一句：
> - 搜索 X 上关于 "ai tool" 的推文 50 条
> - 抓取 @satyanadella 的账号资料
> - 抓取这条推文的评论：https://x.com/...
> - 看看和 @satyanadella 相关的用户

## Scripts

All scripts live at `~/.monsterget/skills/x-collector/scripts/`.

```bash
SCRIPTS="$HOME/.monsterget/skills/x-collector/scripts"
[ -d "$SCRIPTS" ] || { echo "Skill not installed — run the install instruction first." >&2; exit 1; }
```

| Script | Purpose |
|--------|---------|
| `update-skill.sh` | Session start — auto-update check |
| `choose-browser.sh <edge\|chrome>` | Save the user's browser choice |
| `run-scrape.sh <pagePath> <param> <value> [count] [key=value ...]` | Full scrape → CSV |
| `set-download-dir.sh [<dir>]` | Choose where CSVs are saved |

> **🚫 Never run `detect-browser.sh`, `check-login.sh`, or `preflight.sh`.**

### Scrape

```bash
bash "$SCRIPTS/run-scrape.sh" <pagePath> <param> <value> [count] [key=value ...]
```

| Intent | `pagePath` | `param` | `value` | Options |
|--------|-----------|---------|---------|---------|
| Search posts | `/x-search-timeline` | `value` | keyword | `sort=top\|latest` |
| Search users | `/x-search-user` | `value` | keyword | — |
| Profile | `/x-user-profile` | `value` / `values` | `@user` / URL | batch: comma list |
| User tweets | `/x-user-videos-api` | `value` | `@user` | — |
| Tweet detail | `/x-tweet-detail` | `value` / `values` | tweet URL/ID | `export_video`, `export_images`, `export_cover` |
| Tweet comments | `/x-tweet-comments` | `value` / `values` | tweet URL/ID | `comment_sort`, `include_spam` |
| Home feed | `/x-home-timeline` | `-` | empty | `feed=for_you\|following` |

Counts: search 1–100 default 50; user tweets 1–100 default 50; comments 1–1000
default 200; profile/tweet detail 1 per item. Batch max: profile 50, tweet
detail 20, comments 10.

Batch examples:

```bash
bash "$SCRIPTS/run-scrape.sh" /x-user-profile values "@a,@b" 1
MONSTERGET_POLL_TIMEOUT=1800 bash "$SCRIPTS/run-scrape.sh" /x-tweet-comments values "url1,url2" 200 comment_sort=recent
```

The script generates the taskId, opens the browser (fire-and-forget), verifies
the process, polls until ready (default 20 min), and downloads with HTTP/file
verification. It never waits for the user.

Output on success:

```json
{"status":"ready","taskId":"...","file":"...csv","dir":"...","rowCount":50,"empty":false,"url":"..."}
```

## Behavior rules for the agent

- **Open + verify + poll in one shot.** Never ask "is the browser open?".
- **Multiple scrapes = one at a time.** The page already inserts a 3–6s
  anti-detection delay; do not add your own sleep.
- **Show the CSV path + a few rows** so the user trusts the result.
- **First scrape each session**: tell the user once that this drives their real
  X account; the user is responsible for complying with X's terms.
- **Where CSVs are saved**: ask once per machine, then `set-download-dir.sh`.
- **Pre-task reminder**: before every scrape, read `~/.monsterget/state.json`
  and say the reminder from SKILL.md. It is the user's only signal that the
  browser is about to open.

## Common errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `not_found` / `timeout` | Extension missing, not logged in, or tab closed | 3-point manual checklist |
| `platform_reachable: false` | monsterget.com unreachable | Ask user to check the URL |
| `browser did not start` | Launch failed | Ask user to open the URL manually |
| `already_downloaded` | CSV already fetched | Run again (new taskId) |
| `429 too_many_concurrent_scrapes` | Free tier has 1 slot | Wait for running task; page auto-retries |
| Empty fields | Not logged into X | Ask user to confirm X login |
