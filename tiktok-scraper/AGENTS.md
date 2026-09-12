# TikTok Scraper (MonsterGet)

Collect TikTok data (video search, creator search, hashtag search, creator videos, creator profiles) as CSV, driven by an AI agent, scraped through the user's real logged-in browser via the MonsterGet browser extension (anti-ban). Works in any AI client that can run shell commands.

## Language rule

Always reply to the user in the user's own language (zh → 中文, ja → 日本語, es → Español, …).

## When to use

The user asks for TikTok data: videos about X, creators doing X, videos under #tag, all videos by @creator, or creator profile stats — for research, marketing, or content monitoring.

## How it works

```
AI generates taskId ──▶ opens browser URL ──▶ page creates task, extension scrapes ──▶ AI polls status ──▶ AI downloads CSV
```

No server-side TikTok scraping. The scrape runs inside the user's real TikTok session (logged in, with the MonsterGet extension). That's what keeps accounts safe from bans.

## First-run flow (run this right after install)

The user needs 3 things. Do NOT present them as a bullet list they read on their own. Instead:

**a. Silent pre-check.** Run `preflight.sh` once to see what's already done:
```bash
bash ~/.monsterget/skill/scripts/preflight.sh
```

Output fields: `ready` (all done), `next` (first failing step, or `""`), `extension`, `monsterget_login`, `tiktok_login`, `browser`.

**b. Show the 3 prerequisites with links**, noting what's already ✅:

> 用这个 skill 前需要准备 3 件事（都用同一个浏览器：**Edge 或 Chrome**）：
> ① 安装 MonsterGet 扩展 → https://monsterget.com/install
> ② 登录 monsterget.com → https://monsterget.com
> ③ 登录 TikTok → https://www.tiktok.com

**c. Guide one step at a time, starting at `next`.** Per-step protocol: TELL (what to do + URL + which browser) → WAIT for "done" → VERIFY with script → REPORT ✅/❌. Loop until pass, then next. Never advance past a failed step.

| Step | Verify with | URL |
|------|-------------|-----|
| ① Extension | `bash ~/.monsterget/skill/scripts/detect-browser.sh` → `extension:true` | https://monsterget.com/install |
| ② Login MonsterGet | `bash ~/.monsterget/skill/scripts/check-login.sh monsterget` | https://monsterget.com |
| ③ Login TikTok | `bash ~/.monsterget/skill/scripts/check-login.sh tiktok` | https://www.tiktok.com |

If the user says "已装好 / already done", still run the checks. Never trust verbal claims alone.

**d. When all three pass → report + offer example prompts:**

> ✅ 3 项全部通过，可以开始抓取了！
> 试试下面任意一句：
> - 抓取关于 "mike tyson" 的 TikTok 视频 50 条
> - 找出做 "beauty" 内容的 TikTok 创作者 30 个
> - 抓取 #kpop 标签下的视频 30 条
> - 抓取 @tiktok 这位创作者的全部视频
> - 抓取 @mike、@jenifer、@tiktok 的主页数据

## Cold-start contract

`PREFLIGHT_DONE` is `false` at the start of every new conversation. Memory and prior sessions do **not** set it. You must verify programmatically before scraping.

Two entry paths, both ending in verification:
- **First run / user says not set up** → the **First-run flow** above (guide each missing item one at a time: tell → wait for "done" → verify → report; never present a checklist)
- **Setup presumed already done** → run `preflight.sh` silently. If `ready:true`, scrape. If `ready:false`, fall back to the First-run flow starting at `next`.

## Scripts

All scripts live at `~/.monsterget/skill/scripts/`. Resolve once at the start of the session and **exit immediately if not found** — don't proceed without them.

```bash
SCRIPTS="$HOME/.monsterget/skill/scripts"
if [ ! -d "$SCRIPTS" ]; then
  echo "Skill not installed — run the install instruction first." >&2
  exit 1
fi
```

Each script prints one JSON object to stdout and exits 0 on success / 1 on failure.

| Script | Purpose |
|--------|---------|
| `preflight.sh` | Full silent check — extension, platform reachability, both logins. Use when setup is presumed done. |
| `detect-browser.sh` | Extension presence + which browser (edge/chrome/none). Use for step ①. |
| `check-login.sh <target>` | Open login-check page, poll for logged-in status. `target=monsterget` or `tiktok`. Use for steps ②/③. |
| `run-scrape.sh <pagePath> <param> <value> [count]` | Full scrape: generate taskId, open browser, verify process, poll, download CSV. |

### Preflight

```bash
bash ~/.monsterget/skill/scripts/preflight.sh
# → {"ready":false,"next":"extension","extension":true,"platform_reachable":true,
#    "monsterget_login":true,"tiktok_login":true,"browser":"edge","os":"windows"}
```

When `ready` is `false`, read `next` and follow the **First-run flow** above from that step. `next` is empty when `ready` is `true` — the user can scrape immediately.

### Scrape

```bash
bash ~/.monsterget/skill/scripts/run-scrape.sh <pagePath> <param> <value> [count]
```

| Intent | `pagePath` | `param` | `value` example |
|--------|-----------|---------|----------------|
| videos about X | `/tiktok-search-video` | `query` | `mike tyson` |
| creators doing X | `/tiktok-search-user` | `query` | `beauty` |
| videos under #tag | `/tiktok-tag` | `query` | `kpop` (no `#`) |
| videos by @creator | `/tiktok-user-videos` | `username` | `@mike` |
| profile of @creator | `/tiktok-profile` | `username` | `@mike` |
| several profiles | `/tiktok-profile` | `usernames` | `mike,jenifer,tiktok` |

Default counts: video search 50, creator search 30, tag 30, user videos 50. Max: 300.

The script generates the taskId, opens the browser (fire-and-forget), verifies the process started, polls until ready (up to 5 minutes), and downloads the CSV. It never waits for the user.

Output on success: `{"status":"ready","taskId":"...","file":"...csv","rowCount":N,"url":"..."}`

## Behavior rules for the agent

- **Open + verify + poll in one shot.** Never ask "is the browser open?" or "shall I continue?".
- **Don't stop between multiple scrapes.** Run them back-to-back and report everything at the end.
- **Show the CSV path + a few rows** so the user trusts the result.
- **First scrape each session**: tell the user once that this drives their real TikTok account (user's account, user's responsibility).
- **On failure**: use the error field to explain exactly what to fix — don't just say "try again".

## Common errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| `platform_reachable: false` | monsterget.com unreachable | Ask user to check the URL manually |
| `extension: false` | Browser extension not installed | Guide to https://monsterget.com/install |
| `browser did not start` | Launch command failed | Ask user to open the URL manually in the extension browser |
| Not ready in 5 minutes | Extension missing / not logged in / tab closed | Keep the tab open until the scrape finishes |
| `already_downloaded` | CSV already fetched | Run again (new taskId) |
| `429 too_many_concurrent_scrapes` | Free tier has 1 slot | Wait for running task to finish, then retry |