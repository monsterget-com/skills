# 🛡️ MonsterGet Skills — Anti-Ban Web Scraping for AI

> **Stop getting blocked. Scrape TikTok through your real browser — your existing logged-in session. AI-automated, zero-setup, permanently free.**

[![永久免费](https://img.shields.io/badge/🆓-永久免费-22bb33?style=flat-square)](https://monsterget.com)
[![AI Native](https://img.shields.io/badge/🤖-AI%20Native-2196F3?style=flat-square)](https://monsterget.com)
[![10M Credits](https://img.shields.io/badge/📦-注册即享%201000万条-FF9800?style=flat-square)](https://monsterget.com)

---

## ✨ It's what?

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

`Claude Code` · `Codex` · `Cursor` · `Windsurf` · `ChatGPT` · `Cline` · `Aider` · `Continue`

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
| [🎵 tiktok-scraper](tiktok-scraper/SKILL.md) | TikTok video search, creator discovery, hashtag collection, creator profile export to CSV | TikTok |

*More platforms coming (LinkedIn, Instagram, X/Twitter, YouTube…). Open an issue to vote.*

## 🔧 How to Install

```bash
# Claude Code / Codex / Cline
git clone https://github.com/rosstzc/monsterget.com-skills.git
cp -r monsterget.com-skills/tiktok-scraper ~/.claude/skills/

# Other clients — paste the SKILL.md contents into custom-instructions
```

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