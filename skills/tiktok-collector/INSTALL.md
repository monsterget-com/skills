# Installing tiktok-collector

## The fast way (recommended)

Open your AI client and send this in the chat:

> 💬 Install the tiktok-collector skill from https://github.com/monsterget-com/skills

The AI agent will clone and install the skill, then show you a short value menu. Pick a goal and it will guide you through the minimal setup.

## What the AI does (for your verification)

1. `git clone` this repository
2. Copies `skills/tiktok-collector/` → `~/.monsterget/skills/tiktok-collector/`
3. Adds a one-line pointer to your client's custom instructions/rules file

That's it. The actual scripts stay at `~/.monsterget/skills/tiktok-collector/scripts/` so all your AI clients share the same runtime.

> **Multi-skill layout**: skills now live side-by-side under `~/.monsterget/skills/<skill>/` (tiktok-collector, linkedin-collector, …). Each skill is self-contained; the shared `~/.monsterget/state.json` and `~/.monsterget/version.json` carry the browser choice, download dir, and scrapers API version.

> **Migrating from the old single-skill layout** (`~/.monsterget/skill/`)? Move it:
> ```bash
> mkdir -p ~/.monsterget/skills && mv ~/.monsterget/skill ~/.monsterget/skills/tiktok-collector
> ```
> Then update the pointer in your rules file. Both skills' runtimes coexist without conflict.

> **Note**: If you use Claude Code natively, you can also symlink directly:
> `ln -s ~/.monsterget/skills/tiktok-collector ~/.claude/skills/tiktok-collector`

## Manual install

```bash
# Step 1 — clone and copy the runtime (once, shared by all clients)
git clone https://github.com/monsterget-com/skills /tmp/mgs
mkdir -p ~/.monsterget/skills/tiktok-collector
cp -r /tmp/mgs/skills/tiktok-collector/. ~/.monsterget/skills/tiktok-collector/

# Step 2 — point your client at it (pick one)
# Claude Code (native, no pointer needed)
cp -r ~/.monsterget/skills/tiktok-collector ~/.claude/skills/tiktok-collector

# Codex CLI / Cursor / Zed / Windsurf / Copilot / Aider / Gemini CLI
echo 'For TikTok data, read ~/.monsterget/skills/tiktok-collector/SKILL.md' >> AGENTS.md

# Cline
echo 'For TikTok data, read ~/.monsterget/skills/tiktok-collector/SKILL.md' >> .clinerules/

# Roo Code
echo 'For TikTok data, read ~/.monsterget/skills/tiktok-collector/SKILL.md' >> .roo/rules/tiktok-collector.md

# Kilo Code
echo 'For TikTok data, read ~/.monsterget/skills/tiktok-collector/SKILL.md' >> .kilocode/rules/tiktok-collector.md

# Any other client — paste the content of ~/.monsterget/skills/tiktok-collector/SKILL.md into
# your client's custom instructions / rules textarea.
```

## Verify the install

```bash
# Quick check that the SKILL.md and scripts are in place
ls ~/.monsterget/skills/tiktok-collector/SKILL.md && echo "installed"
```
(No automated checks — the AI will guide you manually.)

## First-time user setup (~3 minutes, done once)

The moment the skill is installed, the AI shows a **value menu first** — not the setup steps:

> 装好了 ✅ 先不用配置。
> 你想先用 TikTok 数据达成什么？回复数字：
>
> 1️⃣ 找爆款/竞品打法
> 2️⃣ 找达人/创作者
> 3️⃣ 听用户声音
> 4️⃣ 追标签/趋势
>
> 回复 1–4；不确定就回复"你推荐"。

After you choose, the AI shows a mini plan and asks for **one** input (keyword/tag/creator/video URL). Only then does it show the 3 setup steps:

| Step | What to do | URL |
|------|-----------|-----|
| ① | Install the MonsterGet browser extension | [monsterget.com/install](https://monsterget.com/install) |
| ② | Log in to monsterget.com (same browser) | [monsterget.com](https://monsterget.com) |
| ③ | Log in to TikTok (same browser) | [tiktok.com](https://www.tiktok.com) |

Tell the AI which browser you used and say "好了"; the AI saves your choice. **No automatic checks — you confirm manually.** Then the AI runs a Quick sample and gives you a CSV + Top results + 3 insights, with an option to upgrade to a full Standard analysis.

> 💡 This skill uses **pure manual confirmation** — the AI never scans your disk or opens test windows. You know your browser best. If something fails later, the AI will ask you to check the 3 conditions again — still manually.
>
> This skill uses the shared Agent v2 contract (`scrapers_api` v4; catalog version is a content fingerprint) and
> requires extension **1.8.0+**.
