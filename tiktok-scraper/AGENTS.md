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

## One-time setup (user, ~2 minutes, done once)

1. Register a free account at [monsterget.com](https://monsterget.com)
2. Install the browser extension at [monsterget.com/install](https://monsterget.com/install) (Chrome or Edge — pick one browser and use it for everything)
3. Log in to [monsterget.com](https://monsterget.com) and [www.tiktok.com](https://www.tiktok.com) in that same browser

**Same-browser rule**: the extension, MonsterGet login, and TikTok login must all live in the same browser. Never let the user spread them.

## Cold-start contract

`PREFLIGHT_DONE` is `false` at the start of every new conversation. Memory and prior sessions do **not** set it. You must verify programmatically before scraping.

Two entry paths:
- **No prior knowledge / user says not set up** → interactive Step 0 (guide each missing item one at a time: tell → wait for "done" → verify → report; never present a checklist)
- **Setup presumed already done** → silent preflight (below)

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
# → {"extension":true,"platform_reachable":true,"monsterget_login":true,"tiktok_login":true,"browser":"edge","os":"windows"}
```

If it fails, find which field is `false` and guide the user through only that item (see interactive flow below). Re-verify after the user says "done". Never advance past a failed item.

### Interactive Step 0 (per-step protocol)

For each unfinished step (in order ①→②→③):
1. **TELL** one short message: what to do + the full clickable URL + which browser
2. **WAIT** for the user to say "done"
3. **VERIFY** programmatically — run the check script; do NOT ask "are you sure?"
4. **REPORT** ✅ step N done / ❌ step N failed with fix instructions
5. If ❌ → re-guide → wait → re-verify. Loop until ✅. Do NOT advance.

| Step | Verify script | URL |
|------|---------------|-----|
| ① Install extension | `detect-browser.sh` → `extension:true` | https://monsterget.com/install |
| ② Log in to MonsterGet | `check-login.sh monsterget` | https://monsterget.com |
| ③ Log in to TikTok | `check-login.sh tiktok` | https://www.tiktok.com |

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