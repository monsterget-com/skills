# 🛡️ MonsterGet Skills — Anti-Ban Web Scraping for AI

> **Stop getting blocked. Scrape TikTok through your real browser — your existing logged-in session. AI-automated, zero-setup, permanently free.**

**English** · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Português](README.pt.md)

[![Permanently Free](https://img.shields.io/badge/🆓-Permanently%20Free-22bb33?style=flat-square)](https://monsterget.com)
[![AI Native](https://img.shields.io/badge/🤖-AI%20Native-2196F3?style=flat-square)](https://monsterget.com)
[![10M Credits](https://img.shields.io/badge/📦-10M%20on%20Signup-FF9800?style=flat-square)](https://monsterget.com)
[![Install via npx skills](https://img.shields.io/badge/🧩-Install%20via%20skills.sh-000?style=flat-square)](https://skills.sh)
[![Install via Claude Code](https://img.shields.io/badge/⚡-Install%20via%20Claude%20Code-6B46C1?style=flat-square)](https://github.com/monsterget-com/skills)

---

## ✨ What is it?

**MonsterGet Skills** turn any AI assistant into a TikTok data powerhouse — without your accounts getting banned.

Here's the dirty secret of web scraping: **server-side scrapers get blocked.** TikTok, Instagram, LinkedIn — they all fight headless browsers, datacenter IPs, and proxy pools. You fight back, they block harder. It's an arms race you lose.

MonsterGet flips the game: **the scrape runs inside your own browser**, in your real logged-in session. TikTok sees a real user. You get the data.

| Approach | Anti-ban | Setup | Cost |
|----------|----------|-------|------|
| ❌ Server-side scraper | ❌ Gets blocked | Hours of config | Proxies + infra |
| ❌ Headless browser | ❌ Detected fast | Selenium/Playwright | Server bills |
| ✅ **MonsterGet (your browser)** | ✅ **Invisible** | **2 minutes, one-time** | **🆓 Free tier: 10M entries** |

## 🚀 What can you do with it?

| Use case | Data you get |
|----------|-------------|
| 🔍 **Influencer discovery** | Search creators by keyword → CSV with bio, follower count, avatar |
| 🎬 **Video research** | Search videos by keyword → CSV with plays, likes, comments, share URL |
| 🏷️ **Hashtag intelligence** | Enter a hashtag → CSV of every video under it |
| 👤 **Creator audit** | Get every video a specific creator posted → full analytics |
| 📊 **Bulk profile pull** | 50+ usernames at once → one CSV, aggregated |

All results are clean CSV files — open in Excel, import into your analysis, or feed back to your AI.

## 🤖 AI-Native by Design

Works with **every** major AI coding tool:

`Claude Code` · `Codex CLI` · `Cursor` · `Windsurf` · `Cline` · `Roo Code` · `Kilo Code` · `Copilot` · `Gemini CLI` · `Zed` · `Aider` · `Continue` · `Junie` · `Warp` · `Devin`

The skill is **agent-agnostic by construction**: all shell work lives in protocoled scripts that print JSON, so the same skill behaves identically whether the driving agent is Claude Code or anything else.

The AI orchestrates everything:

```
🧠 AI: "I need TikTok data for market research"
   ↓
🔗 Opens a URL in YOUR browser
   ↓
🌐 Your real TikTok session + MonsterGet extension collects the data
   ↓
📥 AI downloads the CSV and hands it to you
```

**You never touch Python, Selenium, proxies, or captchas.** The AI does the orchestration, your browser does the scraping.

## 🎁 Pricing That Actually Makes Sense

| Tier | Credits | Concurrent Windows | Price |
|------|---------|-------------------|-------|
| Free | **10,000,000** entries | 1 | **🆓 $0 — permanently** |
| Member | More | More parallel | Reasonable |

No tricks. No "free tier" that expires after 14 days. 10 million entries are real.

## 💬 What users say

> *"I was rotating 50 proxies and still getting blocked on TikTok. MonsterGet just works — first time, every time."*
> — **E-commerce data analyst**

> *"Told my Claude to 'find me 200 TikTok creators in the beauty space.' Came back 3 minutes later with a CSV. Didn't write a single line of code."*
> — **Marketing agency owner**

> *"Setup took 2 minutes. I've scraped 2 million entries. Still on the free tier. This feels illegal but apparently it's fine."*
> — **Growth hacker**

## ⏱️ First-time Setup — 2 Minutes, One-Time

| Step | What to do |
|------|-----------|
| 1 | [Register free account](https://monsterget.com) — email + password, done |
| 2 | [Install browser extension](https://monsterget.com/install) — Chrome/Edge, 1 click |
| 3 | Copy a skill folder into your AI client → you're done |

After that, **every scrape is instant.** No more setup. Ever.

## 📦 Available Skills

| Skill | What it does | Platforms |
|-------|--------------|-----------|
| [🎵 tiktok-collector](skills/tiktok-collector/SKILL.md) | TikTok video search, creator discovery, hashtag collection, creator profile export to CSV | TikTok |

*More platforms coming (LinkedIn, Instagram, X/Twitter, YouTube…). Open an issue to vote.*

## 🔧 How to Install

**No commands to memorize.** Open your AI assistant (Claude Code / Codex / Cursor / Cline…), and send this in the chat:

> 💬 Install the tiktok-collector skill from https://github.com/monsterget-com/skills

That's it. The AI clones the repo, installs the runtime, and wires itself up.

### What the AI does

1. Clones this repository
2. Copies `skills/tiktok-collector/` → `~/.monsterget/skill/` — a **shared runtime directory**
3. Adds a one-line pointer to its own custom-instructions file

Because the runtime lives in one shared location (`~/.monsterget/skill/`), **every AI client on your machine shares it**. Install once, use it from Claude Code, Codex, Cursor, Cline — whatever you have.

**Prefer to do it by hand?** See [skills/tiktok-collector/INSTALL.md](skills/tiktok-collector/INSTALL.md) for manual steps and the per-client pointer locations.

**No shell access** (web-only chat like ChatGPT in a browser)? Paste the contents of [`skills/tiktok-collector/SKILL.md`](skills/tiktok-collector/SKILL.md) into your custom instructions — the AI will guide you through the steps manually.

## 🧠 Architecture (what actually happens)

```
AI ──▶ generates taskId + opens browser URL
         │
Your Browser ──▶ MonsterGet extension runs the scrape in your TikTok tab
                   │
                Rows stream to server buffer ──▶ AI polls & downloads CSV
```

**No data ever stored on servers after delivery.** Privacy-first by design.

## 📄 License

MIT — see [LICENSE](LICENSE).

---

> **Ready to stop fighting anti-bot systems?** [Register free →](https://monsterget.com)
>
> *10 million entries. One browser session. Zero blocked accounts.*