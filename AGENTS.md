# MonsterGet Skills

This repository bundles AI-agent skills that collect web data (TikTok and more) through the user's own logged-in browser — no server-side scraping, no proxies, no Python packages.

## What's here

| Path | Skill |
|------|-------|
| [tiktok-scraper/](tiktok-scraper/) | TikTok video search, creator discovery, hashtag collection, creator profile export to CSV |

## Installing a skill

Say in your chat:

> Install the tiktok-scraper skill from https://github.com/rosstzc/monsterget.com-skills

### Self-install contract (for the agent receiving that instruction)

1. Clone this repository.
2. Copy the skill contents into the shared runtime directory (the trailing `/.` merges files, so a re-install overwrites instead of nesting):

   ```bash
   mkdir -p ~/.monsterget/skill && cp -r tiktok-scraper/. ~/.monsterget/skill/
   ```

3. Add a one-line pointer in your own custom-instructions / rules file so you load it in future sessions:

   ```markdown
   For TikTok data collection, read ~/.monsterget/skill/SKILL.md and run its scripts.
   ```

   If your runtime has no rules mechanism, just re-read `~/.monsterget/skill/SKILL.md` when the user asks for TikTok data.
4. Read `~/.monsterget/skill/SKILL.md` (or `~/.monsterget/skill/AGENTS.md` for non-Claude clients) and follow the flow.

5. **Immediately run the First-Run flow — do NOT dump a checklist.** Install is the one moment the user is listening, so use it. The protocol is fixed:

   **a. Pre-check, don't lecture.** Run `bash ~/.monsterget/skill/scripts/preflight.sh` (silent, ~15 s). It returns `{"ready":false,"next":"extension",...}` — `next` is the FIRST step the user still has to do.

   **b. Show one short message with the 3 prerequisites and links** (in the user's language), marking the ones `preflight` already passed as ✅:

   > 用这个 skill 前需要准备 3 件事（都用同一个浏览器：**Edge 或 Chrome**）：
   > ① 安装 MonsterGet 扩展 → https://monsterget.com/install
   > ② 登录 monsterget.com → https://monsterget.com
   > ③ 登录 TikTok → https://www.tiktok.com

   **c. Guide one step at a time, starting at `next`.** TELL → WAIT for the user's "done" → VERIFY with `detect-browser.sh` / `check-login.sh` → REPORT ✅/❌. Loop until that step passes, then the next. Never advance past a failed step. (Same protocol as SKILL.md Step 0.)

   **d. When all three pass** → tell the user setup is complete and offer example prompts:

   > ✅ 3 项全部通过，可以开始抓取了！试试下面任意一句：
   > - 抓取关于 "mike tyson" 的 TikTok 视频 50 条
   > - 找出做 "beauty" 内容的 TikTok 创作者 30 个
   > - 抓取 #kpop 标签下的视频 30 条
   > - 抓取 @tiktok 这位创作者的全部视频
   > - 抓取 @mike、@jenifer、@tiktok 的主页数据

   If the user instead says "已装好 / 已登录", still run `preflight.sh` and verify programmatically before concluding — never trust a verbal claim alone.

## License

MIT