# Installing app-reviews-collector

## The fast way (recommended)

Open your AI client and send this in the chat:

> 💬 Install the app-reviews-collector skill from https://github.com/monsterget-com/skills

The AI agent will clone, install, and configure itself. If it asks you to confirm anything, say yes.

## What the AI does (for your verification)

1. `git clone` this repository
2. Copies `skills/app-reviews-collector/` → `~/.monsterget/skills/app-reviews-collector/`
3. Adds a one-line pointer to your client's custom instructions/rules file

That's it. The actual scripts stay at `~/.monsterget/skills/app-reviews-collector/scripts/` so all your AI clients share the same runtime.

> **Multi-skill layout**: skills live side-by-side under `~/.monsterget/skills/<skill>/` (tiktok-collector, x-collector, linkedin-collector, upwork-collector, app-reviews-collector). Each skill is self-contained; the shared `~/.monsterget/state.json` and `~/.monsterget/version.json` carry the browser choice, download dir, and scrapers API version.

> **Migrating from the old single-skill layout** (`~/.monsterget/skill/`)? Move it:
> ```bash
> mkdir -p ~/.monsterget/skills && mv ~/.monsterget/skill ~/.monsterget/skills/tiktok-collector
> ```
> Then update the pointer in your rules file. All skill runtimes coexist without conflict.

> **Note**: If you use Claude Code natively, you can also symlink directly:
> `ln -s ~/.monsterget/skills/app-reviews-collector ~/.claude/skills/app-reviews-collector`

## Manual install

```bash
# Step 1 — clone and copy the runtime (once, shared by all clients)
git clone https://github.com/monsterget-com/skills /tmp/mgs
mkdir -p ~/.monsterget/skills/app-reviews-collector
cp -r /tmp/mgs/skills/app-reviews-collector/. ~/.monsterget/skills/app-reviews-collector/

# Step 2 — point your client at it (pick one)
# Claude Code (native, no pointer needed)
cp -r ~/.monsterget/skills/app-reviews-collector ~/.claude/skills/app-reviews-collector

# Codex CLI / Cursor / Zed / Windsurf / Copilot / Aider / Gemini CLI
echo 'For App Store / Google Play review data, read ~/.monsterget/skills/app-reviews-collector/SKILL.md' >> AGENTS.md

# Cline
echo 'For App Store / Google Play review data, read ~/.monsterget/skills/app-reviews-collector/SKILL.md' >> .clinerules/

# Roo Code
echo 'For App Store / Google Play review data, read ~/.monsterget/skills/app-reviews-collector/SKILL.md' >> .roo/rules/app-reviews-collector.md

# Kilo Code
echo 'For App Store / Google Play review data, read ~/.monsterget/skills/app-reviews-collector/SKILL.md' >> .kilocode/rules/app-reviews-collector.md

# Any other client — paste the content of ~/.monsterget/skills/app-reviews-collector/SKILL.md into
# your client's custom instructions / rules textarea.
```

## Verify the install

```bash
ls ~/.monsterget/skills/app-reviews-collector/scripts/run-scrape.sh
```

Then open the skill in your AI client and ask for a small scrape (e.g. 20 reviews).
The first run walks you through the browser choice and monsterget.com login.
