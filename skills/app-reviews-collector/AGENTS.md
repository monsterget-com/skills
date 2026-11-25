# App Reviews Collector (MonsterGet)

Collect public **iOS App Store** and **Android Google Play** reviews as CSV, driven by an AI agent, scraped through the user's real browser via the MonsterGet browser extension. No app-store login, no API key, no proxies. Works in any AI client that can run shell commands.

## Language rule

Always reply to the user in the user's own language (zh → 中文, ja → 日本語, es → Español, …).

## ⚠️ Answering "how to use" questions — user-first rule

When the user asks "怎么使用", "how to use this skill", "怎么用爬虫", or anything equivalent asking for usage guidance:

**The user is an end user, not a developer of this skill. Never show them bash commands, script paths (`run-scrape.sh`, `choose-browser.sh`), API endpoints (`monsterget.com/api/…`), taskIds, polling logic, VERSION.json, state.json, or any implementation detail.**

Instead, reply with 4-8 lines of conversational text in the user's language, giving 2-3 example natural-language prompts they can just say:

> 你可以直接对我这样说：
>
> - "抓取 **小红书 App** 在 Google Play 上最近 500 条评论"
> - "抓取这个 App 在 **中国区和日本区** 的 App Store 评论，只看 1-2 星：https://apps.apple.com/cn/app/id741292507"
> - "把 **com.xingin.xhs** 的中文和英文评论各抓 300 条，保留开发者回复"
>
> 我会自动帮你抓取并生成 CSV 文件。需要什么直接说就行。

The implementation details (bash commands, script names, API URLs, polling) are for your execution only — they must never appear in your answer to the user.

## When to use

The user asks for app review / rating data for an iOS or Android app — for product research, competitor analysis, feature prioritization, ASO, sentiment analysis, or customer-support triage. Also use it when the user pastes an App Store / Google Play link and asks "what are people saying".

## How it works

```
AI generates taskId ──▶ opens browser URL ──▶ page creates task, extension fetches public reviews ──▶ AI polls status ──▶ AI downloads CSV
```

There is no server-side scraping. The extension fetches the public review API from inside the app-store page in the user's browser.

## First-run flow (pure manual — no code verification)

The user needs 2 things, both in the **same browser** (the one they chose). The AI shows the guide and the user confirms manually. **No script checks anything.**

**a. Show the setup guide with links** (in the user's language):

> 用这个 skill 前需要准备 2 件事（都用同一个浏览器：**Edge 或 Chrome**）：
> ① 安装 MonsterGet 扩展 → 打开 https://monsterget.com/install 安装
> ② 登录 monsterget.com → 打开 https://monsterget.com 注册并登录
>
> 不需要登录 App Store 或 Google Play —— 评论是公开数据。
> 装好扩展后告诉我装在了哪个浏览器（回复"Edge"或"Chrome"），全部准备好了回复"好了"。

**b. WAIT** for the user to reply with the browser name and "好了". **Never run any detection script, never scan the disk, never verify programmatically.** The user's manual confirmation is the only check.

**c. Save the browser choice** — whatever the user said, save it directly:

```bash
bash ~/.monsterget/skills/app-reviews-collector/scripts/choose-browser.sh edge
# (or chrome — user said Chrome)
# → {"ok":true,"browser":"edge",...}
```

The choice persists across sessions. Never second-guess it with a disk scan.

**d. Confirm + offer example prompts:**

> ✅ 都准备好了，可以开始抓取了！
> 试试下面任意一句：
> - 抓取这个 App 在 App Store 中国区的 500 条评论：https://apps.apple.com/cn/app/id741292507
> - 抓取 **com.xingin.xhs** 在 Google Play 的中文和英文评论各 300 条
> - 只看某 App 的 1-2 星差评，最近半年

If anything is missing later (scrape fails), use the failure checklist in SKILL.md — again, manual only, never a script check.

## Scripts

All scripts live at `~/.monsterget/skills/app-reviews-collector/scripts/`. Resolve once at the start of the session and **exit immediately if not found** — don't proceed without them.

```bash
SCRIPTS="$HOME/.monsterget/skills/app-reviews-collector/scripts"
if [ ! -d "$SCRIPTS" ]; then
  echo "Skill not installed — run the install instruction first." >&2
  exit 1
fi
```

Each script prints one JSON object to stdout and exits 0 on success / 1 on failure.

| Script | Purpose |
|--------|---------|
| `update-skill.sh` | Session start — auto-update check. Compare local version against GitHub, auto-download updates. |
| `choose-browser.sh <edge\|chrome>` | Save the user's browser choice (manual — no verification, saves whatever the user says). |
| `run-scrape.sh <pagePath> <param> <value> [count] [key=value ...]` | Full scrape: generate taskId, open browser, verify process, poll, download CSV. Options carry countries/languages/stars/sort. |
| `set-download-dir.sh [<dir>]` | Choose where scraped CSVs are saved (persists in state). No arg = system Downloads. Ask the user once per machine. |

> **🚫 Never run archived detection scripts** (`detect-browser.sh`, `check-login.sh`, `preflight.sh`). They are not shipped in this skill; the user guarantees all conditions manually.

### Browser choice

During installation the user verbally confirms which browser has the MonsterGet extension; the AI saves it with `choose-browser.sh`. `run-scrape.sh` reads the saved `browser_pref` and opens that browser. No detection, no scanning, no second-guessing.

### Scrape

```bash
bash ~/.monsterget/skills/app-reviews-collector/scripts/run-scrape.sh <pagePath> <param> <value> [count] [key=value ...]
```

| Intent | `pagePath` | `param` | `value` example |
|--------|-----------|---------|----------------|
| iOS App Store reviews | `/app-store-reviews` | `value` | App Store URL or numeric id (`741292507`) |
| Android Google Play reviews | `/google-play-reviews` | `value` | Play URL or package (`com.xingin.xhs`) |

**⚠️ Count rule.**
- `app_store_reviews`: `count` = reviews **per country** (default 500, max 10000). `countries=cn,jp` + `count=500` → up to 1000 rows.
- `google_play_reviews`: `count` = reviews **per language** (default 500, max 5000). `languages=zh-CN,en` + `count=500` → up to 1000 rows.

**Options**

| Option | Default | Meaning |
|--------|---------|---------|
| `countries` | URL country / `us` | App Store storefronts, comma list, max 10 |
| `languages` | `zh-CN,en` | Google Play languages, comma list, max 10 |
| `stars` | all | Star filter `1..5`, comma list (e.g. `1,2`) |
| `since` | empty | App Store only, `YYYY-MM-DD` |
| `sort` | `recent` / `newest` | App Store `recent`/`helpful`; Play `newest`/`helpful` |
| `text_only` | `1` | Keep only reviews with text |
| `include_replies` | `1` | Keep developer replies |
| `delay_ms` | `600` | API request delay (200–3000) |
| `rss_fallback` | `1` | App Store only — RSS fallback when the review API is empty |

The script generates the taskId, opens the browser (fire-and-forget), verifies the process started, polls until ready (default 20 minutes; set `MONSTERGET_POLL_TIMEOUT=3600` for large multi-country/language runs), and downloads with HTTP/file verification. It never waits for the user.

Output on success: `{"status":"ready","taskId":"...","file":"...csv","rowCount":N,"empty":false,"url":"..."}`

## Behavior rules for the agent

- **Open + verify + poll in one shot.** Never ask "is the browser open?" or "shall I continue?".
- **Multiple scrapes = orchestrate them one at a time.** Run the first `run-scrape.sh`, wait for its result, then run the next. The page's `auto=1` flow already inserts a random 3–6s delay before the scraper window opens, so you don't add any sleep — just run each scrape and report between them.
- **Show the CSV path + a few rows** so the user trusts the result.
- **No account-risk warning needed** — reviews are public and no app-store login is used. Still mention that this drives the user's browser through monsterget.com.
- **Where CSVs are saved**: the first time you scrape, ask the user where CSV files should go — "保存到系统下载目录（默认）可以吗？还是换个路径？" Then save their choice with `set-download-dir.sh` (no arg = system Downloads, or pass a path). It persists, so ask at most once per machine; `run-scrape.sh` reports the `dir` in its output.
- **On failure**: use the error field to explain exactly what to fix — don't just say "try again".
- **Pre-task reminder**: before every scrape, read `~/.monsterget/state.json` and say the reminder sentence from SKILL.md — this is the user's only confirmation that the browser is about to open. Never skip it.

## Common errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `not_found` / `timeout` | Extension missing, not logged into monsterget.com, or the tab was closed | Run the 2-point manual checklist (SKILL.md Step 3) |
| `platform_reachable: false` | monsterget.com unreachable | Ask user to check the URL manually |
| `browser did not start` | Launch command failed | Ask user to open the URL manually in the extension browser |
| Not ready within the poll window | Extension missing / not logged in / tab closed / still queued | Keep the tab open until `ready`; for large runs raise `MONSTERGET_POLL_TIMEOUT` |
| `already_downloaded` | CSV already fetched | Run again (new taskId) |
| `429 too_many_concurrent_scrapes` | Free tier has 1 slot | Wait for running task to finish, then retry |
| Empty result | No reviews in that storefront/language, or filters too narrow | Try another country/language, widen the filters, or remove `since` |
