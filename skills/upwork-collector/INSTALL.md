# Installing upwork-collector

## Fast way

> 💬 Install the upwork-collector skill from https://github.com/monsterget-com/skills

## Manual install

```bash
git clone https://github.com/monsterget-com/skills /tmp/mgs
mkdir -p ~/.monsterget/skills/upwork-collector
cp -r /tmp/mgs/skills/upwork-collector/. ~/.monsterget/skills/upwork-collector/
```

Point your client at it:

```bash
# Claude Code (native)
cp -r ~/.monsterget/skills/upwork-collector ~/.claude/skills/upwork-collector

# Codex CLI / Cursor / Zed / Windsurf / Copilot / Aider / Gemini CLI
echo 'For Upwork data, read ~/.monsterget/skills/upwork-collector/SKILL.md' >> AGENTS.md

# Cline
echo 'For Upwork data, read ~/.monsterget/skills/upwork-collector/SKILL.md' >> .clinerules/

# Roo Code
echo 'For Upwork data, read ~/.monsterget/skills/upwork-collector/SKILL.md' >> .roo/rules/upwork-collector.md
```

## First-time user setup (~2 minutes, once)

| Step | What to do | URL |
|------|-----------|-----|
| ① | Install the MonsterGet browser extension | [monsterget.com/install](https://monsterget.com/install) |
| ② | Log in to monsterget.com (same browser) | [monsterget.com](https://monsterget.com) |
| ③ | Log in to Upwork (same browser) | [upwork.com](https://www.upwork.com) |

Tell the AI which browser you used and say "好了". **No automatic checks — you confirm manually.**
Then try: "找一下 Upwork 上关于 'Amazon' 的岗位 10 条".

> This skill uses the shared Agent v2 contract (`scrapers_api` version 4) and
> requires extension **1.8.0+**.
