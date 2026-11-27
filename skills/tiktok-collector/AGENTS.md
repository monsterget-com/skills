# TikTok Collector (MonsterGet)

Collect TikTok data (video search, creator search, hashtag search, creator videos, creator profiles) as CSV, driven by an AI agent, scraped through the user's real logged-in browser via the MonsterGet browser extension (anti-ban). Works in any AI client that can run shell commands.

## Language rule

Always reply to the user in the user's own language (zh → 中文, ja → 日本語, es → Español, …).

## ⚠️ Answering "how to use" questions — value-first rule

When the user asks "怎么使用", "how to use this skill", "怎么用爬虫", "你能做什么", or anything equivalent asking for usage guidance:

**The user is an end user, not a developer of this skill. Never show them bash commands, script paths (`run-scrape.sh`, `choose-browser.sh`), API endpoints (`monsterget.com/api/…`), taskIds, polling logic, VERSION.json, state.json, or any implementation detail.**

Show the 4 business outcomes and ask them to pick one:

> 你可以用 TikTok 数据做这 4 类事：
>
> 1️⃣ 找爆款/竞品打法 — 抓热门视频，按互动率找选题
> 2️⃣ 找达人/创作者 — 按内容方向找创作者，看粉丝和互动
> 3️⃣ 听用户声音 — 抓视频评论，找真实需求/不满
> 4️⃣ 追标签/趋势 — 看某个标签最近什么内容在涨
>
> 回复 1–4；不确定就回复"你推荐"。

Do not open with setup steps. Only after the user picks do you show the mini plan and the setup they need. The full flow and copy bank are in `ONBOARDING.md`.

## When to use

The user asks for TikTok data: videos about X, creators doing X, videos under #tag, all videos by @creator, or creator profile stats — for research, marketing, or content monitoring.

## How it works

```
AI generates taskId ──▶ opens browser URL ──▶ page creates task, extension scrapes ──▶ AI polls status ──▶ AI downloads CSV
```

No server-side TikTok scraping. The scrape runs inside the user's real TikTok session (logged in, with the MonsterGet extension). That's what keeps accounts safe from bans.

## First-run flow (value first — no setup wall)

**Read `ONBOARDING.md` before the first user-facing message.** The first message sells outcomes, not setup. The full flow, copy bank, branches, and acceptance checklist live there; this section is the short version.

**a. Show the value menu** (in the user's language) — 4 TikTok business outcomes, 0 setup steps:

> 装好了 ✅ 先不用配置。
> 你想先用 TikTok 数据达成什么？回复数字：
>
> 1️⃣ 找爆款/竞品打法
>    抓关键词或竞品账号下的热门视频，按互动率找选题
>
> 2️⃣ 找达人/创作者
>    按内容方向找创作者，看粉丝和互动
>
> 3️⃣ 听用户声音
>    抓视频评论，找真实需求/不满
>
> 4️⃣ 追标签/趋势
>    看某个标签最近什么内容在涨
>
> 回复 1–4；不确定就回复"你推荐"。

**b. WAIT** for the user to choose. Then show the mini plan for that choice — deliverable, Quick sample size, and time. Do not show setup yet.

**c. Ask exactly one input** — keyword, competitor account, creator handle, or video URL. Always offer "你推荐".

If the user already gave a direct task ("抓取 mike tyson 50 条"), skip the menu and start at the mini plan with that input.

**d. Just-in-time setup** — only after the input, show the 3 things (extension, monsterget.com login, TikTok login) and save the browser choice. **Never run any detection script, never scan the disk, never verify programmatically.** The user's manual confirmation is the only check.

**e. First sample + deliver** — run a Quick sample, label it "小样/Quick", then show the CSV path + Top results + 3 insights and a next-step menu (deepen / switch / done).

**f. Persist** — save goal/sub/input/stage with `set-onboarding.sh` so the next session can offer "继续上次的吗？".

### Mini plan example (choice 1)

> 好，选「找爆款/竞品打法」。
>
> 先跑一个 3–5 分钟的小样（Quick 档，明确标注是小样）：
> - 50 条相关视频：标题/播放/点赞/评论/发布时间
> - 按互动率排序，给你 Top 10
> - 3 个可复制的选题方向
>
> 只需要 1 个信息：关键词或竞品账号。
> 没有的话回复"你推荐"，我先用行业默认词。

### Delivery example

> 结果好了 ✅
> - 50 条视频，Top 3 互动率：...
> - CSV：...
> - 3 个可复制选题：...
>
> 下一步：
> A. 扩到 250–300 条，做完整分析（Standard）
> B. 换一个关键词/竞品对比
> C. 换一个目标

## Scripts

All scripts live at `~/.monsterget/skills/tiktok-collector/scripts/`. Resolve once at the start of the session and **exit immediately if not found** — don't proceed without them.

```bash
SCRIPTS="$HOME/.monsterget/skills/tiktok-collector/scripts"
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
| `set-onboarding.sh key value [key value ...]` | Persist onboarding goal/sub/input/stage for the value-first flow (`goal`, `sub`, `input`, `stage`). |
| `run-scrape.sh <pagePath> <param> <value> [count] [key=value ...]` | Full scrape: generate taskId, open browser, verify process, poll, download CSV. Extra options cover comments/detail flags. |
| `set-download-dir.sh [<dir>]` | Choose where scraped CSVs are saved (persists in state). No arg = system Downloads. Ask the user once per machine. |

> **🚫 Never run `detect-browser.sh`, `check-login.sh`, or `preflight.sh`** — archived reference only. The user guarantees all conditions manually. The AI must not call them during installation, before a scrape, or on failure.

### Browser choice

During onboarding — after the user chooses a goal and gives the input — the user verbally confirms which browser has the MonsterGet extension; the AI saves it with `choose-browser.sh`. `run-scrape.sh` reads the saved `browser_pref` and opens that browser. No detection, no scanning, no second-guessing.

### Scrape

```bash
bash ~/.monsterget/skills/tiktok-collector/scripts/run-scrape.sh <pagePath> <param> <value> [count] [key=value ...]
```

| Intent | `pagePath` | `param` | `value` example |
|--------|-----------|---------|----------------|
| videos about X | `/tiktok-search-video` | `query` | `mike tyson` |
| creators doing X | `/tiktok-search-user` | `query` | `beauty` |
| videos under #tag | `/tiktok-tag` | `query` | `kpop` (no `#`) |
| videos by @creator | `/tiktok-user-videos` | `username` | `@mike` |
| profile of @creator | `/tiktok-profile` | `username` | `@mike` |
| several profiles | `/tiktok-profile` | `usernames` | `mike,jenifer,tiktok` |
| comments on a video | `/tiktok-comments` | `value` | video URL |
| details of a video | `/tiktok-video-detail` | `value` / `values` | video URL(s) |

Default counts: video search 50, creator search 30, tag 30, user videos 50,
comments 50, video detail 20. Max: 300 (comments 200, video detail 50).
Comments support `include_replies=0|1`, `max_replies=N`; video detail supports
`export_video=0|1`, `export_cover=0|1`, `export_audio=0|1`.

The script generates the taskId, opens the browser (fire-and-forget), verifies the process started, polls until ready (default 20 minutes; set `MONSTERGET_POLL_TIMEOUT=1800` for long batches), and downloads with HTTP/file verification. It never waits for the user.

Output on success: `{"status":"ready","taskId":"...","file":"...csv","rowCount":N,"empty":false,"url":"..."}`

## Behavior rules for the agent

- **First message = value menu.** Never open with setup steps. The user picks a business outcome before seeing any installation instruction — unless they already stated a direct task; then acknowledge it and go to the mini plan/input.
- **One input at a time.** After the user chooses a goal, ask only for the one input the task needs (keyword, competitor, handle, tag, or URL). Always offer "你推荐/用默认".
- **First sample is Quick and labeled.** Deliver the CSV + Top results + 3 insights, then offer the Standard tier. Never call a Quick sample a full report.
- **Returning users**: read `tiktok_onboarding_*` from `~/.monsterget/state.json` and offer "继续上次的吗？" before showing the menu again.
- **Open + verify + poll in one shot.** Never ask "is the browser open?" or "shall I continue?".
- **Multiple scrapes = orchestrate them one at a time.** Run the first `run-scrape.sh`, wait for its result, then run the next. The page's `auto=1` flow already inserts a random 3–6s delay before the scraper window opens (anti-detection), so you don't add any sleep — just run each scrape and report between them.
- **Show the CSV path + a few rows** so the user trusts the result.
- **First scrape each session**: tell the user once that this drives their real TikTok account (user's account, user's responsibility).
- **Where CSVs are saved**: the first time you scrape, ask the user where CSV files should go — "保存到系统下载目录（默认）可以吗？还是换个路径？" Then save their choice with `set-download-dir.sh` (no arg = system Downloads, or pass a path). It persists, so ask at most once per machine; `run-scrape.sh` reports the `dir` in its output.
- **On failure**: use the error field to explain exactly what to fix — don't just say "try again".
- **Pre-task reminder**: before every scrape, read `~/.monsterget/state.json` and say the reminder sentence from SKILL.md — this is the user's only confirmation that the browser is about to open. Never skip it.

## Common errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `not_found` / `timeout` | Extension missing, not logged in, or the tab was closed | Run the failure checklist in `SKILL.md` (`### 3. On failure — user checklist`) — the user checks each in the browser by hand |
| `platform_reachable: false` | monsterget.com unreachable | Ask user to check the URL manually |
| `browser did not start` | Launch command failed | Ask user to open the URL manually in the extension browser |
| Not ready within the poll window | Extension missing / not logged in / tab closed / still queued | Keep the tab open until `ready`; the extension auto-closes after completion |
| `already_downloaded` | CSV already fetched | Run again (new taskId) |
| `429 too_many_concurrent_scrapes` | Free tier has 1 slot | Wait for running task to finish, then retry |
