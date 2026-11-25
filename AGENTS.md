# MonsterGet Skills

This repository bundles AI-agent skills that collect web data (TikTok, X/Twitter,
LinkedIn, Upwork) through the user's own logged-in browser — no server-side
scraping, no proxies, no Python packages.

## What's here

| Path | Skill | Coverage |
|------|-------|----------|
| [skills/tiktok-collector/](skills/tiktok-collector/) | TikTok video/creator/hashtag/profile/comments/detail | 7 types |
| [skills/x-collector/](skills/x-collector/) | X search/profiles/user tweets/tweet detail/comments/home feed | 7 types |
| [skills/linkedin-collector/](skills/linkedin-collector/) | LinkedIn profile, similar-people recommendations, job search, people search, job detail | 5 types |
| [skills/upwork-collector/](skills/upwork-collector/) | Upwork job search (single/multi-page, auto-all) | 1 type |
| [skills/app-reviews-collector/](skills/app-reviews-collector/) | iOS App Store + Android Google Play reviews (multi-country/language) | 2 types |

Together they cover the 22 scrapers exposed by the platform Agent API
(`scrapers_api` version 4; extension **1.8.0+**, **1.12.0+** for app-store reviews).

## Installing a skill

Say in your chat:

> Install the tiktok-collector skill from https://github.com/monsterget-com/skills
>
> Install the x-collector skill from https://github.com/monsterget-com/skills
>
> Install the linkedin-collector skill from https://github.com/monsterget-com/skills
>
> Install the upwork-collector skill from https://github.com/monsterget-com/skills
>
> Install the app-reviews-collector skill from https://github.com/monsterget-com/skills

### Self-install contract (for the agent receiving that instruction)

1. Clone this repository.
2. Copy the requested skill into the shared runtime directory under its
   per-skill folder (the trailing `/.` merges files, so a re-install overwrites
   instead of nesting):

   ```bash
   mkdir -p ~/.monsterget/skills/<skill> && cp -r skills/<skill>/. ~/.monsterget/skills/<skill>/
   ```

   Skills live side-by-side: `~/.monsterget/skills/tiktok-collector/`,
   `~/.monsterget/skills/x-collector/`, `~/.monsterget/skills/linkedin-collector/`,
   `~/.monsterget/skills/upwork-collector/`, `~/.monsterget/skills/app-reviews-collector/`.
   Each is self-contained. The shared
   `~/.monsterget/state.json` (browser choice, download dir) and
   `~/.monsterget/version.json` (scrapers API version) carry cross-skill settings.

3. Add a one-line pointer in your own custom-instructions / rules file:

   ```markdown
   For TikTok data, read ~/.monsterget/skills/tiktok-collector/SKILL.md and run its scripts.
   For X/Twitter data, read ~/.monsterget/skills/x-collector/SKILL.md and run its scripts.
   For LinkedIn data, read ~/.monsterget/skills/linkedin-collector/SKILL.md and run its scripts.
   For Upwork data, read ~/.monsterget/skills/upwork-collector/SKILL.md and run its scripts.
   For App Store / Google Play reviews, read ~/.monsterget/skills/app-reviews-collector/SKILL.md and run its scripts.
   ```

4. Read the requested skill's `SKILL.md` (or `AGENTS.md` for non-Claude clients)
   and follow its flow.

5. **Immediately run that skill's First-Run flow.** Install is the one moment
   the user is listening. The skill's `AGENTS.md` contains the exact setup guide
   (install extension → log in monsterget.com → log in the target site when
   required; app-store reviews need no store login), the manual confirmation
   step, and `choose-browser.sh`.

   **Never run detection scripts, scan the disk, or verify programmatically** —
   the user's manual confirmation is the only check.

## Shared Agent contract

- All skills use the same `run-scrape.sh` protocol:
  `run-scrape.sh <pagePath> <param> <value> [count] [key=value ...]`
- The AI discovers the live catalog from `GET /api/agent/scrapers` (version 4).
- Only the types whose `platform` matches the skill are used.
- Agent work is isolated behind `task_type='agent'` and
  `auto=1&agentTaskId`; manual scraping on the platform is unchanged.

## License

MIT
