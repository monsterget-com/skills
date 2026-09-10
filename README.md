# MonsterGet Skills

Public skills for **MonsterGet** — the anti-ban web scraping platform.

These skills let **any AI assistant** (Claude Code, Codex, Cursor, Windsurf, ChatGPT…) collect
web data on the user's behalf: the AI orchestrates a task, the user's own browser does the
scraping inside their real logged-in session, and the result comes back as a CSV.

No Python packages. No credentials. No headless setup.

## Available skills

| Skill | What it does | Platforms |
|-------|--------------|-----------|
| [tiktok-scraper](tiktok-scraper/SKILL.md) | TikTok video search, creator discovery, hashtag collection, creator profiles | TikTok |

## Install

Copy the skill folder into your AI client's skills directory:

```bash
# Claude Code
git clone https://github.com/rosstzc/monsterget.com-skills.git
cp -r monsterget.com-skills/tiktok-scraper ~/.claude/skills/
```

For other clients (Codex, Cursor, Windsurf, ChatGPT), paste the contents of the skill's
`SKILL.md` into your client's custom-instructions or skill slot.

## How it works

```
AI ──1. GET {SITE_URL}/api/agent/generate-task-id ──▶ {"taskId":"<uuid>"}
AI ──2. open browser page  {pagePath}?auto=1&agentTaskId={taskId}&{param}=...&count=N
Page (user browser, logged in + extension) ──▶ creates the task
Extension executes the scrape in the target tab
Page relays rows to the server buffer
AI ──3. GET {SITE_URL}/api/agent/delivery/task/{taskId}/status  ──▶ {status:"ready"}
AI ──4. GET {SITE_URL}/api/agent/delivery/task/{taskId}/data    ──▶ CSV download
```

## First-time setup (one-time, ~2 minutes)

1. Register a free account at [monsterget.com](https://monsterget.com)
2. Install the MonsterGet browser extension from [monsterget.com/install](https://monsterget.com/install)

After that, every scrape is repeatable and instant.

## Contributing

This repository is a **publish mirror**. Skill sources are maintained in the MonsterGet
platform repository and synced here on release. To report a problem or request a new skill,
please open an issue.

## License

MIT — see [LICENSE](LICENSE).