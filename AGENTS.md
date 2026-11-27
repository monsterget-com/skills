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

### Business skills (v2 preview)

Collectors get data; business skills turn data into a decision. The flow is:

```text
monsterget-context  ->  monsterget-business  ->  voc-miner / freelance-lead-radar / ...
```

| Path | Skill | What it does |
|------|-------|--------------|
| [skills/monsterget-context/](skills/monsterget-context/) | Business context | Brand, product, ICP, voice, guardrails -> `.agents/monsterget-context.md` |
| [skills/monsterget-business/](skills/monsterget-business/) | Router | Picks the right business skill and estimates data/time |
| [skills/voc-miner/](skills/voc-miner/) | VOC Miner | TikTok/X comments + App Store/Play reviews -> evidence-backed VOC report |
| [skills/freelance-lead-radar/](skills/freelance-lead-radar/) | Freelance Lead Radar | Upwork jobs -> ranked leads + proposal drafts |

Business skills do **not** duplicate the collector runtime. Each business skill
ships `scripts/resolve-runtime.sh` and uses it to find the collector:

```bash
SKILL_DIR="${MONSTERGET_HOME:-$HOME/.monsterget}/skills/voc-miner"
[ -d "$SKILL_DIR" ] || SKILL_DIR=".agents/skills/voc-miner"
RUN_SCRAPE="$(bash "$SKILL_DIR/scripts/resolve-runtime.sh" tiktok-collector)"
bash "$RUN_SCRAPE" /tiktok-search-video query "..." 50
```

**Data volume:** every business skill defaults to **Standard** (1,000–2,000
analyzed items), with Quick/Deep tiers. Read
[DATA-STANDARDS.md](DATA-STANDARDS.md) before planning a scrape; never silently
run a demo-sized sample for a real report.

v2 is on the `v2` branch until the first design-partner cases pass.

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
>
> Install the monsterget-context skill from https://github.com/monsterget-com/skills
>
> Install the monsterget-business skill from https://github.com/monsterget-com/skills
>
> Install the voc-miner skill from https://github.com/monsterget-com/skills
>
> Install the freelance-lead-radar skill from https://github.com/monsterget-com/skills

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
   `~/.monsterget/skills/upwork-collector/`, `~/.monsterget/skills/app-reviews-collector/`,
   plus business skills under `~/.monsterget/skills/monsterget-context/`,
   `~/.monsterget/skills/monsterget-business/`, `~/.monsterget/skills/voc-miner/`,
   `~/.monsterget/skills/freelance-lead-radar/`.
   Each is self-contained. The shared
   `~/.monsterget/state.json` (browser choice, download dir) and
   `~/.monsterget/version.json` (scrapers API version) carry cross-skill settings.

   **Business skill dependencies:** install the collectors it needs first
   (`voc-miner` -> `tiktok-collector`, `x-collector`, `app-reviews-collector`;
   `freelance-lead-radar` -> `upwork-collector`). Business skills find the
   collector runtime with `scripts/resolve-runtime.sh`.

3. Add a one-line pointer in your own custom-instructions / rules file:

   ```markdown
   For TikTok data, read ~/.monsterget/skills/tiktok-collector/SKILL.md and run its scripts.
   For X/Twitter data, read ~/.monsterget/skills/x-collector/SKILL.md and run its scripts.
   For LinkedIn data, read ~/.monsterget/skills/linkedin-collector/SKILL.md and run its scripts.
   For Upwork data, read ~/.monsterget/skills/upwork-collector/SKILL.md and run its scripts.
   For App Store / Google Play reviews, read ~/.monsterget/skills/app-reviews-collector/SKILL.md and run its scripts.
   For business context, read ~/.monsterget/skills/monsterget-context/SKILL.md first.
   For business research, read ~/.monsterget/skills/monsterget-business/SKILL.md and route to the right skill.
   ```

4. Read the requested skill's `SKILL.md` (or `AGENTS.md` for non-Claude clients)
   and follow its flow.

5. **Immediately run that skill's First-Run flow.** Install is the one moment
   the user is listening. The skill's `AGENTS.md` contains the exact flow. If it
   defines a **value-first onboarding** (e.g. `tiktok-collector`), start with the
   value menu and show the setup only after the user chooses a goal. Otherwise
   follow its setup guide (install extension → log in monsterget.com → log in the
   target site when required; app-store reviews need no store login), the manual
   confirmation step, and `choose-browser.sh`.

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
