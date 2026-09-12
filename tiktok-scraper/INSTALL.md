# Installing tiktok-scraper

## The fast way (recommended)

Open your AI client and send this in the chat:

> 💬 Install the tiktok-scraper skill from https://github.com/rosstzc/monsterget.com-skills

The AI agent will clone, install, and configure itself. If it asks you to confirm anything, say yes.

## What the AI does (for your verification)

1. `git clone` this repository
2. Copies `tiktok-scraper/` → `~/.monsterget/skill/`
3. Adds a one-line pointer to your client's custom instructions/rules file

That's it. The actual scripts stay at `~/.monsterget/skill/scripts/` so all your AI clients share the same runtime.

> **Note**: If you use Claude Code natively, you can also symlink directly:
> `ln -s ~/.monsterget/skill ~/.claude/skills/tiktok-scraper`

## Manual install

```bash
# Step 1 — clone and copy the runtime (once, shared by all clients)
git clone https://github.com/rosstzc/monsterget.com-skills /tmp/mgs
mkdir -p ~/.monsterget
cp -r /tmp/mgs/tiktok-scraper ~/.monsterget/skill

# Step 2 — point your client at it (pick one)
# Claude Code (native, no pointer needed)
cp -r ~/.monsterget/skill ~/.claude/skills/tiktok-scraper

# Codex CLI / Cursor / Zed / Windsurf / Copilot / Aider / Gemini CLI
echo 'For TikTok data, read ~/.monsterget/skill/SKILL.md' >> AGENTS.md

# Cline
echo 'For TikTok data, read ~/.monsterget/skill/SKILL.md' >> .clinerules/

# Roo Code
echo 'For TikTok data, read ~/.monsterget/skill/SKILL.md' >> .roo/rules/tiktok-scraper.md

# Kilo Code
echo 'For TikTok data, read ~/.monsterget/skill/SKILL.md' >> .kilocode/rules/tiktok-scraper.md

# Any other client — paste the content of ~/.monsterget/skill/SKILL.md into
# your client's custom instructions / rules textarea.
```

## Verify the install

```bash
# Run the silent preflight (safe, no user interaction needed)
bash ~/.monsterget/skill/scripts/preflight.sh
```

It should print JSON with your current setup status. If `extension: false`, you need to install the browser extension first (see below).

## First-time user setup (~2 minutes, done once)

After installing the skill, the user needs:

| Step | What to do | URL |
|------|-----------|-----|
| 1 | Register a free account | [monsterget.com](https://monsterget.com) |
| 2 | Install the browser extension | [monsterget.com/install](https://monsterget.com/install) |
| 3 | Log in to TikTok | [tiktok.com](https://www.tiktok.com) |

The AI will guide you through these interactively when you first ask it to scrape data.