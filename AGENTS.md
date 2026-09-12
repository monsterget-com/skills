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
5. Tell the user the skill is installed and that they need:
   - A free account at [monsterget.com](https://monsterget.com)
   - The browser extension from [monsterget.com/install](https://monsterget.com/install)
   - The extension, MonsterGet login, and TikTok login all in the **same browser**

## License

MIT