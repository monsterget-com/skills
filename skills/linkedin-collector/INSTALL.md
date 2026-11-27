# Installing linkedin-collector

## The fast way (recommended)

Open your AI client and send this in the chat:

> 💬 Install the linkedin-collector skill from https://github.com/monsterget-com/skills

The AI agent will clone, install, and configure itself. If it asks you to confirm anything, say yes.

## What the AI does (for your verification)

1. `git clone` this repository
2. Copies `skills/linkedin-collector/` → `~/.monsterget/skills/linkedin-collector/`
3. Adds a one-line pointer to your client's custom instructions/rules file

That's it. The actual scripts stay at `~/.monsterget/skills/linkedin-collector/scripts/` so all your AI clients share the same runtime.

> **Multi-skill layout**: skills now live side-by-side under `~/.monsterget/skills/<skill>/` (tiktok-collector, linkedin-collector, …). Each skill is self-contained; the shared `~/.monsterget/state.json` and `~/.monsterget/version.json` carry the browser choice, download dir, and scrapers API version.

> **Migrating from the old single-skill layout** (`~/.monsterget/skill/`)? Move it:
> ```bash
> mkdir -p ~/.monsterget/skills && mv ~/.monsterget/skill ~/.monsterget/skills/tiktok-collector
> ```
> Then update the pointer in your rules file. Both skills' runtimes coexist without conflict.

> **Note**: If you use Claude Code natively, you can also symlink directly:
> `ln -s ~/.monsterget/skills/linkedin-collector ~/.claude/skills/linkedin-collector`

## Manual install

```bash
# Step 1 — clone and copy the runtime (once, shared by all clients)
git clone https://github.com/monsterget-com/skills /tmp/mgs
mkdir -p ~/.monsterget/skills/linkedin-collector
cp -r /tmp/mgs/skills/linkedin-collector/. ~/.monsterget/skills/linkedin-collector/

# Step 2 — point your client at it (pick one)
# Claude Code (native, no pointer needed)
cp -r ~/.monsterget/skills/linkedin-collector ~/.claude/skills/linkedin-collector

# Codex CLI / Cursor / Zed / Windsurf / Copilot / Aider / Gemini CLI
echo 'For LinkedIn data, read ~/.monsterget/skills/linkedin-collector/SKILL.md' >> AGENTS.md

# Cline
echo 'For LinkedIn data, read ~/.monsterget/skills/linkedin-collector/SKILL.md' >> .clinerules/

# Roo Code
echo 'For LinkedIn data, read ~/.monsterget/skills/linkedin-collector/SKILL.md' >> .roo/rules/linkedin-collector.md

# Kilo Code
echo 'For LinkedIn data, read ~/.monsterget/skills/linkedin-collector/SKILL.md' >> .kilocode/rules/linkedin-collector.md

# Any other client — paste the content of ~/.monsterget/skills/linkedin-collector/SKILL.md into
# your client's custom instructions / rules textarea.
```

## Verify the install

```bash
# Quick check that the SKILL.md and scripts are in place
ls ~/.monsterget/skills/linkedin-collector/SKILL.md && echo "installed"
```
(No automated checks — the AI will guide you manually.)

## First-time user setup (~2 minutes, done once)

The moment the skill is installed, the AI **guides you** through 3 manual steps (no code checks, you just confirm):

You need 3 things, all in the **same browser** (Edge or Chrome — pick one):

| Step | What to do | URL |
|------|-----------|-----|
| ① | Install the MonsterGet browser extension | [monsterget.com/install](https://monsterget.com/install) |
| ② | Log in to monsterget.com (same browser) | [monsterget.com](https://monsterget.com) |
| ③ | Log in to LinkedIn (same browser) | [linkedin.com](https://www.linkedin.com) |

Tell the AI which browser you used, say "好了", and the AI saves your choice. **No automatic checks — you confirm manually.** Then the AI offers example prompts — e.g. "抓取 LinkedIn 用户 adrienbeaulieu 的档案".

> 💡 This skill uses **pure manual confirmation** — the AI never scans your disk or opens test windows. You know your browser best. If something fails later, the AI will ask you to check the 3 conditions again — still manually.
>
> This skill uses the shared Agent v2 contract (`scrapers_api` v4; catalog version is a content fingerprint) and
> requires extension **1.8.0+**.
