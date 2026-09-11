---
name: tiktok-scraper
description: 🎁 Permanently free — 10M entries on signup, 1 concurrent window. Zero-install skill: open a browser URL, the extension + logged-in session do the rest. TikTok video search, creator discovery, hashtag collection, user video export to CSV. Works with Claude Code, Codex, Cursor, Windsurf, ChatGPT (any AI client). No Python packages, no credentials, no headless setup.
---

# TikTok Scraper

> 🎁 **永久免费 · 注册即享 1000万条额度 · 免费用户 1 个并发窗口**
> *(Permanently free · 10 million entries on signup · 1 concurrent window for free users. Members unlock more parallel windows.)*

## What is this?

A skill that lets **any AI assistant** (Claude Code, Codex, Cursor, Windsurf, ChatGPT…) scrape TikTok data — video search, creator discovery, hashtag collection, or a specific creator's videos — and return it as a CSV. You don't install Python packages, configure headless browsers, or manage credentials. The AI orchestrates: it generates a task ID, opens a URL in the **user's own browser**, and downloads the result.

**Why a browser + extension?** The actual scrape runs inside the user's real TikTok session (logged in, with the [MonsterGet](https://monsterget.com) browser extension installed). That's what keeps the accounts anti-ban safe. There is no server-side TikTok scraping — the data is collected right where the user is already logged in.

**First-time setup (one-time, ~2 minutes):** the user registers a free account at [monsterget.com](https://monsterget.com) and installs the extension (Chrome/Edge). Everything after that is repeatable and instant.

Scrape TikTok data through the MonsterGet platform running on the user's machine — **zero install, zero credentials, zero Python packages for the user**. The scrape runs in the **user's real browser** with an installed extension and logged-in session (anti-ban core). The AI just orchestrates.

## When to use

User wants TikTok data: video search, user/creator search, hashtag/tag search, or a specific creator's videos — typically for market research, competitor analysis, influencer discovery, content monitoring.

## Architecture (what actually happens)

```
AI ──1. GET {SITE_URL}/api/agent/generate-task-id ──▶ {"taskId":"<uuid>"}
AI ──2. open browser page  {pagePath}?auto=1&agentTaskId={taskId}&{param}=...&count=N
Page (user browser, logged in + extension) ──▶ POST /api/agent/scrape  (creates task with our taskId)
Extension executes scrape in TikTok tab
Page relays rows to server buffer
AI ──3. GET {SITE_URL}/api/agent/delivery/task/{taskId}/status  ──▶ {status:"ready"}
AI ──4. GET {SITE_URL}/api/agent/delivery/task/{taskId}/data    ──▶ CSV download
```

**Key invariant (v0.5):** the AI generates the taskId itself *before* opening the browser, so it never needs to read the browser address bar.

## Configuration

```text
BASE_URL       = https://monsterget.com      # API host (usually same as SITE_URL)
DEFAULT_BROWSER = msedge                     # msedge | chrome | open (mac) | xdg-open (linux)
```

Change `SITE_URL`/`BASE_URL` when the platform is running locally (`http://localhost:8000`).

## Scrape types

> ⚠️ **This table may be stale.** New scrapers are NOT auto-synced into this skill file. Before mapping the user's request to a type, fetch the live list (zero-auth, read-only) and use it if it differs from the table:
> ```bash
> curl -s {BASE_URL}/api/agent/scrapers
> ```
> Use the `type` + `page` + `param` + `countMax` values returned. The table below is a snapshot that matches current scrapers.

| Type | pagePath | Param | Default count | Max |
|------|----------|-------|---------------|-----|
| Video search | `/tiktok-search-video` | `query` | 50 | 300 |
| Creator search | `/tiktok-search-user` | `query` | 30 | 300 |
| Hashtag search | `/tiktok-tag` | `query` | 30 | 300 |
| Creator videos | `/tiktok-user-videos` | `username` | 50 | 300 |
| Creator profile | `/tiktok-profile` | `username` | 1 | 1 |

Username accepts `@name` or full profile URL (server normalizes).

## The full flow

> 🚨 **首次使用四步法（严格按顺序执行）**
>
> ```
> ┌─────────────────────────────────────────────────────────────────┐
> │  首次请求爬虫                                                    │
> │     │                                                            │
> │     ├── Step 0: 打印首次准备清单 → 等用户说"好了"                 │
> │     │    (安装扩展 + 登录 MonsterGet + 登录 TikTok)              │
> │     │                                                            │
> │     ├── Step 0.5: 自动检测循环                                   │
> │     │     while (有未通过项):                                     │
> │     │       检测所有项 → 全部通过? → Yes 跳出                     │
> │     │       No → 列出未通过项 + 引导用户 → 等用户说"好了" → 重测  │
> │     │                                                            │
> │     ├── Step 1~3: 正常执行爬虫                                  │
> │     │                                                            │
> │     └── 首次爬虫成功后 → 标记 Preflight 已完成                    │
> │         同 session 后续爬虫请求直接到 Step 1，跳过 Step 0/0.5     │
> └─────────────────────────────────────────────────────────────────┘
> ```

### ⚡ Automation contract (read this first)

**Opening the browser is fire-and-forget. Never pause to ask the user "is it open?" or "shall I continue?"**

Once you run the browser-open command, the page executes on its own — it creates the task with the taskId you already hold and the extension runs it. Your job is to *immediately* start polling. There is nothing to wait for.

Rules that make the AI fast instead of slow:

1. **Open + poll in one shot.** Run the browser-open command and the poll loop together (see Step 3c). Do not put a message to the user between them.
2. **Never wait for user confirmation** after opening the browser. The user does not need to do anything (unless they aren't logged in yet — that's the one exception, and it shows up as the scrape never reaching `ready`).
3. **Polling already detects completion.** The poll loop exits the moment the status is `ready` (or `failed`). You do not need to ask the user whether the task finished — the status endpoint tells you.
4. **Multiple scrapes run back-to-back, unattended.** When the user asks for several scrapes, run them in a loop: open → poll → download → open the next one. Do **not** stop and report back between tasks. See "Running multiple scrapes" below.
5. **A finished task frees the concurrency slot.** The scrape window may stay open — it does not block the next task. Only a task still `pending`/`processing` counts against the limit.
6. **Only speak to the user** when: first-time setup (Step 0–0.5), a scrape fails, or all requested scrapes are done and you're presenting results.

### Step 0 — 🚀 首次准备清单（仅首次，等用户确认）

> **💡 SKIP RULE**: 如果 `PREFLIGHT_DONE=true`（当前 session 已成功完成过首次爬虫），跳过 Step 0 / 0.5，直接到 Step 1。

告诉用户需要完成 3 件事才开始：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🚀 首次使用准备（仅需做一次）

  请按以下顺序完成 3 步：

  ① 安装 MonsterGet 浏览器扩展
     打开 {SITE_URL}/install，按指引安装到 Edge 浏览器

  ② 登录 monsterget.com
     打开 {SITE_URL}，注册/登录您的账号（或使用游客登录）

  ③ 在浏览器中登录 TikTok
     打开 https://www.tiktok.com，登录您的 TikTok 账号
     （如果只使用非 TikTok 爬虫，此步可跳过）

  完成后请回复"好了"，我来自动检测。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

等待用户回复"好了"或确认完成后，进入 Step 0.5。

### Step 0.5 — 🔄 自动检测循环（仅首次）

> 从 Step 0 收到用户确认后执行。**不单独调用**——必须紧跟 Step 0。

检测三项，结果分为"通过/未通过"。**全部通过 → 告诉用户后跳 Step 1**。有未通过项 → 列出 + 引导 → 等用户"好了" → **只重检测未通过项** → 循环直至全部通过。

#### 检测函数速查

```bash
# ① 扩展安装检测（shell 本地扫描，不需要开浏览器）
_check_extension() {
  EDGE_EXT=$(grep -l "MonsterGet" "$HOME/AppData/Local/Microsoft/Edge/User Data/Default/Preferences" 2>/dev/null || echo "")
  CHROME_EXT=$(grep -l "MonsterGet" "$HOME/AppData/Local/Google/Chrome/User Data/Default/Preferences" 2>/dev/null || echo "")
  if [ -n "$EDGE_EXT" ] || [ -n "$CHROME_EXT" ]; then echo "ok"; else echo "missing"; fi
}

# ② MonsterGet 登录检测（需开浏览器页面回报）
_check_monsterget_login() {
  local MG_ID=$(curl -s "$BASE_URL/api/agent/generate-task-id" | sed -n 's/.*"taskId":"\([^"]*\)".*/\1/p')
  start msedge "$SITE_URL/login-check.html?auto=1&agentTaskId=$MG_ID"
  for i in $(seq 1 12); do
    local R=$(curl -s "$BASE_URL/api/agent/login-check/$MG_ID")
    echo "$R" | grep -q '"logged_in"' && { echo "$R"; return; }
    sleep 5
  done
  echo '{"logged_in":false}'
}

# ③ 目标站（TikTok）登录检测（需开浏览器页面回报）
_check_target_login() {
  local T=$(curl -s -X POST "$BASE_URL/api/agent/login-check-target" \
    -H "Content-Type: application/json" -d '{"target":"tiktok"}')
  local TK_ID=$(echo "$T" | sed -n 's/.*"taskId":"\([^"]*\)".*/\1/p')
  start msedge "$SITE_URL/login-check-target.html?auto=1&agentTaskId=$TK_ID&target=tiktok"
  for i in $(seq 1 12); do
    local R=$(curl -s "$BASE_URL/api/agent/login-check/$TK_ID")
    echo "$R" | grep -q '"logged_in"' && { echo "$R"; return; }
    sleep 5
  done
  echo '{"logged_in":false}'
}
```

#### 循环逻辑

```python
# Python 伪代码 — 按此逻辑执行
checks = {
    "extension": {"fn": _check_extension, "guide": "打开 {SITE_URL}/install 安装扩展"},
    "monsterget": {"fn": _check_monsterget_login, "guide": "打开 {SITE_URL} 登录"},
    "target_tiktok": {"fn": _check_target_login, "guide": "在浏览器登录 https://www.tiktok.com"},
}

# 首次检测全部三项；后续循环只测 failed_items
failed_items = list(checks.keys())

while True:
    current_fails = []
    for name in failed_items:
        c = checks[name]
        result = shell(c["fn"])
        if name == "extension":
            if result == "missing": current_fails.append(name)
        elif name == "monsterget":
            if "false" in result: current_fails.append(name)
        elif name == "target_tiktok":
            if "false" in result: current_fails.append(name)

    if not current_fails:
        tell_user "✅ 全部检测通过！开始抓取..."
        PREFLIGHT_DONE=true  # 记录 session 变量
        break

    # 有未通过的项
    tell_user "以下项目未通过："
    for name in current_fails:
        tell_user f"  ❌ {name}: {checks[name]['guide']}"
    tell_user "完成后请回复'好了'，我将重新检测未通过项。"

    wait_user_reply_ok()
    failed_items = current_fails  # 下一轮只测这些

# 跳出循环后 → 进入 Step 1
```

#### 实际执行指引

1. **先后顺序**：先跑 ①（扩展，最快，不需开浏览器）→ ②（MonsterGet 登录）→ ③（TikTok 登录）。
   - 如果 ① 未通过，**阻止** ② 和 ③（扩展不在，后两项必失败），直接报"扩展未安装"。
2. **轮询超时**：每项最长等 60 秒（12 次 × 5 秒）。超时视为失败。
3. **用户等待**：每次检测开浏览器后立即进入轮询，不打断用户。
4. **成功后标记**：`PREFLIGHT_DONE=true`，同 session 后续抓取**直接跳到 Step 1**，不再引导/检测。

### Step 1 — 平台可达性检测

> 💡 如果 `PREFLIGHT_DONE=true`，**这是本次抓取的第一个步骤**（跳过 Step 0/0.5）。

Quickly probe whether the platform is reachable:

```bash
# Reachability
curl -s -o /dev/null -w "%{http_code}" {BASE_URL}/api/agent/generate-task-id
```

- `200` → reachable. Continue.
- Anything else → tell the user the platform isn't reachable yet. For local: ask them to start the backend. Then stop.

If scraping previously failed with an extension error, ask the user to verify the extension is installed and the browser is logged in (see Troubleshooting).

### Step 2 — 首次准备（已合入 Step 0）

> ✅ 首次引导 + 检测循环已在 Step 0 → 0.5 中完成。此处不再重复。
>
> 如果用户报告扩展缺失或登录问题，参考 Step 0 的引导清单：
> - 安装扩展：`{SITE_URL}/install`
> - 登录 MonsterGet：`{SITE_URL}`
> - 登录目标站（TikTok）：`https://www.tiktok.com`

### Step 3 — Run a scrape (repeatable)

#### 3a. Generate a taskId (zero-auth, no token needed)

```bash
TASK_ID=$(curl -s {BASE_URL}/api/agent/generate-task-id | sed -n 's/.*"taskId":"\([^"]*\)".*/\1/p')
echo "taskId=$TASK_ID"
```

Keep this id — it is the key for everything that follows.

#### 3b. Determine page and params from the user's request

Map intent → `{pagePath}?auto=1&agentTaskId={TASK_ID}&{param}={value}&count={N}`:

| User intent | pagePath | param |
|-------------|----------|-------|
| "videos about X" / "search X" | `/tiktok-search-video` | `query=X` |
| "TikTok users/creators doing X" | `/tiktok-search-user` | `query=X` |
| "#tag videos" / "topic X" | `/tiktok-tag` | `query=X` (drop the `#`) |
| "videos by @creator" | `/tiktok-user-videos` | `username=@creator` |
| "profile of @creator" | `/tiktok-profile` | `username=@creator` |

If count isn't given, use the type default (30 for tag/user search, 50 for video/user-videos). Cap at 300. Path segment separator is a **hyphen** (`/tiktok-search-video`), never an underscore.

#### 3c. Open the page in the chosen browser — **fire-and-forget**

⚠️ **URL must be wrapped in double quotes** — otherwise the shell treats `&` as a command separator and truncates the query.

```bash
# Edge (Windows) — or substitute chrome / open / xdg-open (which browser has the extension)
start msedge "https://monsterget.com/tiktok-search-video?auto=1&agentTaskId=$TASK_ID&query=mike&count=10"
```

If `start` isn't available, use the full exe path:
```bash
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" "https://monsterget.com/tiktok-search-video?auto=1&agentTaskId=$TASK_ID&query=mike&count=10"
```

> 🚀 **Do NOT wait after opening the browser.** The command returning means the browser process was launched — that's all you need. Do not ask the user "is it open?", do not pause, do not read the URL bar. The page creates the task with the taskId you already hold and runs automatically. **Go straight to Step 3d and poll.**

#### 3d. Poll until ready — **start immediately, start in the background**

Open the browser **and start polling in the same step**. Use your tool's run_in_background feature for the poll loop so it works while you can still interact with the user (or start the next task in serial mode):

```bash
# Bash / Mac / Linux — poll every 5s, up to 60 times (5-minute timeout)
for i in $(seq 1 60); do
  STATUS=$(curl -s "https://monsterget.com/api/agent/delivery/task/$TASK_ID/status")
  echo "$STATUS" | grep -q '"status":"ready"' && break
  echo "$STATUS" | grep -qE '"status":"(downloaded|failed)"|not_found' && break
  sleep 5
done
```

```bat
:: Windows cmd — poll every 5s, up to 60 times (5-minute timeout)
for /l %i in (1,1,60) do (
  curl -s "https://monsterget.com/api/agent/delivery/task/$TASK_ID/status" | find "ready"
  if not errorlevel 1 goto download
  timeout /t 5 /nobreak >nul
)
:download
```

Status meanings:
| status | meaning |
|--------|---------|
| `processing` | still running → keep polling |
| `ready` | data ready → download |
| `downloaded` | already fetched → can't re-download |

Response example: `{"taskId":"...","status":"ready","filename":"mike-10-20260905_tiktok_video_ab12cd.csv","resultCount":10,"terminal":true}`

#### 3e. Download the CSV

```bash
curl -OJ "https://monsterget.com/api/agent/delivery/task/$TASK_ID/data"
```

`-OJ` uses the server's semantic filename (`Content-Disposition`). The file is tombstoned after one download (repeat → HTTP 410). Download is only available for 24h.

#### 3f. Verify & present

Show the user the first rows of the CSV so they can confirm the data is correct. State the saved file path.

### Step 4 — Bulk creator profiles (optional)

When the user needs profile data for **multiple creators at once** (e.g., "get profiles of @mike, @jenifer, @tiktok"), use bulk mode with comma-separated usernames:

```bash
TASK_ID=$(curl -s {BASE_URL}/api/agent/generate-task-id | sed -n 's/.*"taskId":"\([^"]*\)".*/\1/p')
start msedge "https://monsterget.com/tiktok-profile?auto=1&agentTaskId=$TASK_ID&usernames=mike,jenifer,tiktok&count=3"
```

The platform creates a **parent task** that chains through each profile sequentially. Poll and download using `$TASK_ID` — the CSV contains one row per creator with aggregated profile stats.

### Running multiple scrapes (serial batch)

When the user asks for **several scrapes at once** (e.g. "test all 5 scrapers"), run them **back-to-back in a loop, unattended**:

```
1. TASK_ID = generate-task-id
2. open browser page 1          (fire-and-forget)
3. poll until ready             (background)
4. download CSV 1
5. TASK_ID = generate-task-id
6. open browser page 2          ← do NOT wait for the user between tasks
7. poll → download
... repeat ...
```

Key rules:
- **Do not stop to ask the user between tasks.** Each new scrape is independent and the concurrency slot frees as soon as the previous one is `ready`.
- The old browser tab may stay open — **it does not block anything**. Close tabs only if you want to reduce clutter.
- Only **serialize if the user has 1 concurrent window** (free tier). If you get a `429 too_many_concurrent_scrapes`, it means a previous task is still `pending`/`processing` — wait for it to be `ready`/`failed`, then continue.
- Report all results **at the end**, together, not one at a time.

## Error handling

| Symptom | Cause | Fix |
|---------|-------|-----|
| `curl` returns nothing / connection refused | platform not reachable | confirm backend running (local) or site is up (production) |
| status endpoint → `404 delivery_not_found` | wrong taskId | re-run 3a and regenerate |
| status stays `processing` > 5 min | extension missing, browser not logged in, or page closed | confirm extension installed + logged in + page still open; page must stay open until scrape completes |
| status endpoint never reaches `ready`, page shows "extension not ready" | extension not installed / not enabled | install extension from `{SITE_URL}/install`, reload page |
| page shows "please log in" | not logged in | log in on `{SITE_URL}`, reopen page |
| Step 0.5 检测 ③ TikTok 未通过 | 浏览器未登录 TikTok | 在 TikTok 登录后回复"好了"，AI 重测 |
| download → `409 not_ready` | data not ready | keep polling |
| download → `409 buffer_unavailable` | buffer cleared by TTL race | retry a few seconds |
| download → `410 already_downloaded` | already fetched once | do NOT retry; regenerate a taskId and run a new scrape |
| 429 too_many_concurrent_scrapes | a previous task is still pending/processing | free users have 1 concurrent window — wait for the running task to reach `ready`/`failed`, then retry. Closing the browser tab is NOT required; a finished task already frees the slot |
| 402 insufficient_credits | credits exhausted | signup grants 10M credits — almost never runs out; need more? contact the platform |

## Concurrency note

Free-tier users have **1 concurrent scrape window** (plenty for daily use). Member tiers can run **up to 10 in parallel**.

The limit counts **running tasks**, not open windows:
- A task counts while it is `pending` or `processing` (the extension is still working).
- The moment a task reaches `ready`, the slot is **freed** — you can open the next scrape right away.
- **An open browser tab with a finished task does NOT block the next task.** Leave tabs open; there is no need to close them.
- A `pending` task that was never claimed (extension not ready / page abandoned) auto-expires after ~30 seconds.

## Gotchas

- **Use the extension-installed browser.** Never rely on the system default browser — it may not have the extension. Ask once, remember the answer.
- **Never call `POST /api/agent/scrape` yourself.** The page does it automatically with your taskId. Calling it manually is not needed and requires auth.
- **Never run headless / sandbox scraping.** Scrapes execute in the user's real browser for anti-ban. If you're sandboxed and can't open a local browser, tell the user to run a local AI terminal (Claude Code CLI, local Codex).
- **Keep the tab open** until the task reaches `ready`. Closing the tab before the extension reports results means no server copy is produced.
- **Do not wait for the user between scrapes.** Open → poll → download → next, all in one uninterrupted run.
- After downloading, show the user the CSV path and a preview so they trust the result.

## Sources

- Platform: [monsterget.com](https://monsterget.com)
- Skill repository: [github.com/rosstzc/monsterget.com-skills](https://github.com/rosstzc/monsterget.com-skills)
