# Migration Notes

## I already use the collectors. Do I need to reinstall?

**No.** The 5 collectors and their runtime are unchanged:

- `tiktok-collector`
- `x-collector`
- `linkedin-collector`
- `upwork-collector`
- `app-reviews-collector`

Your `~/.monsterget/skills/<collector>/` folders, `state.json`, and
`version.json` keep working.

## How do I add the business skills?

Install them the same way as a collector:

```text
Install the monsterget-context skill from https://github.com/monsterget-com/skills
Install the monsterget-business skill from https://github.com/monsterget-com/skills
Install the voc-miner skill from https://github.com/monsterget-com/skills
Install the freelance-lead-radar skill from https://github.com/monsterget-com/skills
```

The AI copies `skills/<skill>/.` to `~/.monsterget/skills/<skill>/`.

Business skills do not include the browser runtime. They find the collector with
`scripts/resolve-runtime.sh`, which checks:

```text
~/.monsterget/skills/<collector>/scripts/run-scrape.sh
.agents/skills/<collector>/scripts/run-scrape.sh
~/.agents/skills/<collector>/scripts/run-scrape.sh
.claude/skills/<collector>/scripts/run-scrape.sh
~/.claude/skills/<collector>/scripts/run-scrape.sh
.codex/skills/...
.cursor/skills/...
.windsurf/skills/...
.opencode/skills/...
```

## What should I install for each business skill?

| Business skill | Collectors it needs |
|---|---|
| `voc-miner` | `tiktok-collector`, `x-collector`, `app-reviews-collector` |
| `freelance-lead-radar` | `upwork-collector` |
| `creator-due-diligence` (planned) | `tiktok-collector`, `x-collector` |
| `competitor-teardown` (planned) | `tiktok-collector`, `x-collector` |
| `aso-pulse` (planned) | `app-reviews-collector` |
| `talent-map` (planned) | `linkedin-collector` |

## I installed the old single-skill layout

Move it once:

```bash
mkdir -p ~/.monsterget/skills
mv ~/.monsterget/skill ~/.monsterget/skills/tiktok-collector
```

Then update the pointer in your rules file.

## I use `npx skills add`

```bash
npx skills add monsterget-com/skills --skill tiktok-collector
npx skills add monsterget-com/skills --skill monsterget-context
npx skills add monsterget-com/skills --skill monsterget-business
npx skills add monsterget-com/skills --skill voc-miner
npx skills add monsterget-com/skills --skill freelance-lead-radar
```

`npx` installs into `.agents/skills/`; the resolver checks that path too.

## v2 branch

The business skills are on the `v2` branch until the first design-partner cases
pass. Collectors on `main` are unchanged. After merge, the same install commands
work without a branch.
