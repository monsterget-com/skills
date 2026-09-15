# MonsterGet Skills

This repository bundles AI-agent skills that collect web data (TikTok and more) through the user's own logged-in browser — no server-side scraping, no proxies, no Python packages.

## What's here

| Path | Skill |
|------|-------|
| [tiktok-collector/](tiktok-collector/) | TikTok video search, creator discovery, hashtag collection, creator profile export to CSV |

## Installing a skill

Say in your chat:

> Install the tiktok-collector skill from https://github.com/monsterget-com/skills

### Self-install contract (for the agent receiving that instruction)

1. Clone this repository.
2. Copy the skill contents into the shared runtime directory (the trailing `/.` merges files, so a re-install overwrites instead of nesting):

   ```bash
   mkdir -p ~/.monsterget/skill && cp -r tiktok-collector/. ~/.monsterget/skill/
   ```

3. Add a one-line pointer in your own custom-instructions / rules file so you load it in future sessions:

   ```markdown
   For TikTok data collection, read ~/.monsterget/skill/SKILL.md and run its scripts.
   ```

   If your runtime has no rules mechanism, just re-read `~/.monsterget/skill/SKILL.md` when the user asks for TikTok data.
4. Read `~/.monsterget/skill/SKILL.md` (or `~/.monsterget/skill/AGENTS.md` for non-Claude clients) and follow the flow.

5. **Immediately run the First-Run flow.** Install is the one moment the user is listening, so use it. Order matters — show the guide BEFORE checking anything:

   **a. Show the full 3-step guide with links** (in the user's language), so the user knows what to prepare:

   > 用这个 skill 前需要准备 3 件事（都用同一个浏览器：**Edge 或 Chrome**）：
   > ① 安装 MonsterGet 扩展 → 打开 https://monsterget.com/install 安装
   > ② 登录 monsterget.com → 打开 https://monsterget.com 注册并登录
   > ③ 登录 TikTok → 打开 https://www.tiktok.com 登录你的账号
   >
   > 准备好了回复"好了"（或"已装好/已登录"），我会自动检测。

   **b. WAIT** for the user to say they're ready. Do not run checks before this — the user needs the guide first.

   **c. VERIFY everything** with the silent pre-check: `bash ~/.monsterget/skill/scripts/preflight.sh`. It returns `{"ready":false,"next":"extension",...}` — `next` is the FIRST step the user still has to do; `ready:true` means all pass. If `next:"choose_browser"`, both browsers have the extension — ask the user which to use, run `choose-browser.sh edge|chrome`, then re-run `preflight.sh`.

   **d. Guide only what's ❌, one step at a time, starting at `next`.** TELL → WAIT for "done" → VERIFY with `detect-browser.sh` / `check-login.sh` → REPORT ✅/❌. Loop until that step passes, then the next. Never advance past a failed step. (Same protocol as SKILL.md Step 0.)

   **e. When all three pass** → tell the user setup is complete and offer example prompts:

   > ✅ 3 项全部通过，可以开始抓取了！试试下面任意一句：
   > - 抓取关于 "mike tyson" 的 TikTok 视频 50 条
   > - 找出做 "beauty" 内容的 TikTok 创作者 30 个
   > - 抓取 #kpop 标签下的视频 30 条
   > - 抓取 @tiktok 这位创作者的全部视频
   > - 抓取 @mike、@jenifer、@tiktok 的主页数据

   If the user instead says "已装好 / 已登录", still run `preflight.sh` and verify programmatically before concluding — never trust a verbal claim alone.

## License

MIT