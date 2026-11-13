# Installing x-collector

## Fast way

Open your AI client and send this in the chat:

> 💬 Install the x-collector skill from https://github.com/monsterget-com/skills

The AI agent will clone, install, and configure itself.

## Manual install

```bash
git clone https://github.com/monsterget-com/skills /tmp/mgs
mkdir -p ~/.monsterget/skills/x-collector
cp -r /tmp/mgs/skills/x-collector/. ~/.monsterget/skills/x-collector/
```

Point your client at it:

```bash
# Claude Code (native)
cp -r ~/.monsterget/skills/x-collector ~/.claude/skills/x-collector

# Codex CLI / Cursor / Zed / Windsurf / Copilot / Aider / Gemini CLI
echo 'For X/Twitter data, read ~/.monsterget/skills/x-collector/SKILL.md' >> AGENTS.md

# Cline
echo 'For X/Twitter data, read ~/.monsterget/skills/x-collector/SKILL.md' >> .clinerules/

# Roo Code
echo 'For X/Twitter data, read ~/.monsterget/skills/x-collector/SKILL.md' >> .roo/rules/x-collector.md
```

## First-time user setup (~2 minutes, once)

| Step | What to do | URL |
|------|-----------|-----|
| ① | Install the MonsterGet browser extension | [monsterget.com/install](https://monsterget.com/install) |
| ② | Log in to monsterget.com (same browser) | [monsterget.com](https://monsterget.com) |
| ③ | Log in to X (same browser) | [x.com](https://x.com) |

Tell the AI which browser you used and say "好了". **No automatic checks — you confirm manually.**
Then try: "搜索 X 上关于 'ai tool' 的推文 50 条".

> This skill uses the shared Agent v2 contract (`scrapers_api` version 3) and
> requires extension **1.8.0+**.
