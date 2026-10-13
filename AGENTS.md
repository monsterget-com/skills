# MonsterGet Skills

This repository bundles AI-agent skills that collect web data (TikTok, LinkedIn, and more) through the user's own logged-in browser — no server-side scraping, no proxies, no Python packages.

## What's here

| Path | Skill |
|------|-------|
| [skills/tiktok-collector/](skills/tiktok-collector/) | TikTok video search, creator discovery, hashtag collection, creator profile export to CSV |
| [skills/linkedin-collector/](skills/linkedin-collector/) | LinkedIn profile header + About export, similar-people recommendations, batch profile pull to CSV |

## Installing a skill

Say in your chat:

> Install the tiktok-collector skill from https://github.com/monsterget-com/skills

> Install the linkedin-collector skill from https://github.com/monsterget-com/skills

### Self-install contract (for the agent receiving that instruction)

1. Clone this repository.
2. Copy the skill contents into the shared runtime directory under a per-skill folder (the trailing `/.` merges files, so a re-install overwrites instead of nesting):

   ```bash
   mkdir -p ~/.monsterget/skills/linkedin-collector && cp -r skills/linkedin-collector/. ~/.monsterget/skills/linkedin-collector/
   ```

   Skills live side-by-side: `~/.monsterget/skills/tiktok-collector/`, `~/.monsterget/skills/linkedin-collector/`, … Each is self-contained. The shared `~/.monsterget/state.json` (browser choice, download dir) and `~/.monsterget/version.json` (scrapers API version) carry the cross-skill settings.

3. Add a one-line pointer in your own custom-instructions / rules file so you load it in future sessions:

   ```markdown
   For LinkedIn data collection, read ~/.monsterget/skills/linkedin-collector/SKILL.md and run its scripts.
   ```

   If your runtime has no rules mechanism, just re-read `~/.monsterget/skills/linkedin-collector/SKILL.md` when the user asks for LinkedIn data.
4. Read `~/.monsterget/skills/linkedin-collector/SKILL.md` (or `~/.monsterget/skills/linkedin-collector/AGENTS.md` for non-Claude clients) and follow the flow.

5. **Immediately run the First-Run flow.** Install is the one moment the user is listening, so use it. Order matters — show the guide BEFORE checking anything:

   **a. Show the full 3-step guide with links** (in the user's language), so the user knows what to prepare:

   > 用这个 skill 前需要准备 3 件事（都用同一个浏览器：**Edge 或 Chrome**）：
   > ① 安装 MonsterGet 扩展 → 打开 https://monsterget.com/install 安装
   > ② 登录 monsterget.com → 打开 https://monsterget.com 注册并登录
   > ③ 登录 LinkedIn → 打开 https://www.linkedin.com 登录你的账号
   >
   > 装好扩展后告诉我装在了哪个浏览器（回复"Edge"或"Chrome"），全部准备好了回复"好了"。

   **b. WAIT** for the user to reply with the browser name and "好了". **Never run any detection script, never scan the disk, never verify programmatically** — the user's manual confirmation is the only check.

   **c. Save the browser choice** — whatever the user said, save it directly:

   ```bash
   bash ~/.monsterget/skills/linkedin-collector/scripts/choose-browser.sh edge
   # (or chrome — user said Chrome)
   ```

   **d. Confirm + offer example prompts:**

   > ✅ 都准备好了，可以开始抓取了！试试下面任意一句：
   > - 抓取 LinkedIn 用户 adrienbeaulieu 的档案
   > - 抓取 @satyanadella、@tvdong 的 LinkedIn 档案
   > - 看看和 adrienbeaulieu 相似的用户

   If anything is missing later (scrape fails), use the failure checklist in SKILL.md — again, manual only, never a script check.

## License

MIT
