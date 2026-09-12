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

The moment the skill is installed, the AI **immediately guides** you through the 3 steps — one at a time, verifying each before moving on. You will see this in chat:

| Step | What to do | URL |
|------|-----------|-----|
| ① | Install the MonsterGet browser extension (Edge or Chrome) | [monsterget.com/install](https://monsterget.com/install) |
| ② | Log in to monsterget.com (same browser) | [monsterget.com](https://monsterget.com) |
| ③ | Log in to TikTok (same browser) | [tiktok.com](https://www.tiktok.com) |

All 3 must pass the AI's automatic checks before it lets you scrape. When they do, the AI offers example prompts — e.g. "抓取关于 'mike tyson' 的 TikTok 视频 50 条".

If your client just printed this table as static text instead of walking you through it step by step, that's a weak client — the checks still protect you, but you can say "检查一下这 3 项" to force the programmatic verification.