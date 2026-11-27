# 🛡️ MonsterGet Skills — Anti-Ban Web Scraping for AI

> **Stop getting blocked. Scrape TikTok, X/Twitter, LinkedIn, Upwork, the App Store & Google Play through your real browser — your existing session. AI-automated, zero-setup, permanently free.**

**English** · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [Español](README.es.md) · [Português](README.pt.md)

[![Permanently Free](https://img.shields.io/badge/🆓-Permanently%20Free-22bb33?style=flat-square)](https://monsterget.com)
[![AI Native](https://img.shields.io/badge/🤖-AI%20Native-2196F3?style=flat-square)](https://monsterget.com)
[![10M Credits](https://img.shields.io/badge/📦-10M%20on%20Signup-FF9800?style=flat-square)](https://monsterget.com)
[![Install via npx skills](https://img.shields.io/badge/🧩-Install%20via%20skills.sh-000?style=flat-square)](https://skills.sh)
[![Install via Claude Code](https://img.shields.io/badge/⚡-Install%20via%20Claude%20Code-6B46C1?style=flat-square)](https://github.com/monsterget-com/skills)

---

## ✨ What is it?

**MonsterGet Skills** turn any AI assistant into a multi-platform data powerhouse — TikTok, X/Twitter, LinkedIn, Upwork, the App Store and Google Play — without your accounts getting banned.

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
| 💼 **LinkedIn profiles** | Profile header + full About text → one row per profile |
| 🧑‍💼 **LinkedIn similar people** | "More profiles for you" recommendations → name, headline, connection |
| 🔎 **LinkedIn jobs** | Job search by URL, 25 per page, multi-page / auto-all |
| 👥 **LinkedIn people** | People search by keyword, location, industry → name, headline, profile URL |
| 🐦 **X/Twitter research** | Search feeds, profiles, user tweets, tweet details, comments, home feed |
| 💼 **Upwork jobs** | Job search results by URL, one or many pages, auto-all |
| 🍎 **App Store reviews** | iOS reviews by app + country → rating, title, text, developer replies |
| 🤖 **Google Play reviews** | Android reviews by app + language → rating, text, version, helpful votes |

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

## 📚 Real Case Studies — Step-by-Step, with Real Data

> Every case study is an actual scraping session I ran myself. You get the exact dialog I used, the raw CSV output, and the analysis that came out of it.

| # | Topic | What You'll Learn |
|---|-------|-------------------|
| 1 | [Competitor Analysis](skills/tiktok-collector/case-studies/01-competitor-analysis.md) | Scrape a brand's last 100 videos, find their best-performing content categories |
| 2 | [Creator Discovery: Two-Step Funnel](skills/tiktok-collector/case-studies/02-creator-discovery.md) | Search content first → extract creators → deep-dive each one's 50 videos + engagement rates |
| 3 | [Follower Count Is a Lie](skills/tiktok-collector/case-studies/03-fake-follower-exposed.md) | Two creators side by side — 144k followers vs 73k, but the smaller one has 74× more real reach |

[📂 View All Case Studies →](skills/tiktok-collector/case-studies/)

## ⏱️ First-time Setup — 2 Minutes, One-Time

| Step | What to do |
|------|-----------|
| 1 | [Register free account](https://monsterget.com) — email + password, done |
| 2 | [Install browser extension](https://monsterget.com/install) — Chrome/Edge, 1 click |
| 3 | Copy a skill folder into your AI client → you're done |

After that, **every scrape is instant.** No more setup. Ever.

## 📦 Available Skills

| Skill | What it does | Types |
|-------|--------------|-------|
| [🎵 tiktok-collector](skills/tiktok-collector/SKILL.md) | Video search, creator discovery, hashtags, creator videos/profiles, video comments and details | 7 |
| [🐦 x-collector](skills/x-collector/SKILL.md) | Search feeds, user search, profiles, user tweets, tweet details, tweet comments, home feed | 7 |
| [💼 linkedin-collector](skills/linkedin-collector/SKILL.md) | Profile header + About, similar-people recommendations, batch pulls, job search, people search, job detail | 5 |
| [💼 upwork-collector](skills/upwork-collector/SKILL.md) | Job search by URL, one/many pages, auto-all | 1 |
| [⭐ app-reviews-collector](skills/app-reviews-collector/SKILL.md) | iOS App Store + Android Google Play reviews, multi-country/language | 2 |

**22 scrapers total**, all through the same Agent API (`scrapers_api` v4; the catalog version is a content fingerprint that auto-updates — currently `19144`; extension **1.8.0+**, **1.12.0+** for App Store / Google Play reviews). More platforms will be added as the platform exposes
them to the Agent API.

## 🔧 How to Install

**No commands to memorize.** Open your AI assistant (Claude Code / Codex / Cursor / Cline…), and send this in the chat:

> 💬 Install the tiktok-collector skill from https://github.com/monsterget-com/skills

> 💬 Install the x-collector skill from https://github.com/monsterget-com/skills

> 💬 Install the linkedin-collector skill from https://github.com/monsterget-com/skills

> 💬 Install the upwork-collector skill from https://github.com/monsterget-com/skills

> 💬 Install the app-reviews-collector skill from https://github.com/monsterget-com/skills

That's it. The AI clones the repo, installs the runtime, and wires itself up.

### What the AI does

1. Clones this repository
2. Copies `skills/<skill>/` → `~/.monsterget/skills/<skill>/` — a **shared runtime directory** (one folder per skill, side-by-side)
3. Adds a one-line pointer to its own custom-instructions file

Because the runtime lives in one shared location (`~/.monsterget/skills/`), **every AI client on your machine shares it**. Install once, use it from Claude Code, Codex, Cursor, Cline — whatever you have.

**Prefer to do it by hand?** See the `INSTALL.md` inside each skill folder for manual steps and per-client pointer locations.

**No shell access** (web-only chat like ChatGPT in a browser)? Paste the contents of the chosen `skills/<skill>/SKILL.md` into your custom instructions — the AI will guide you through the steps manually.

> **Migrating from the old single-skill layout** (`~/.monsterget/skill/`)? Move it once:
> ```bash
> mkdir -p ~/.monsterget/skills && mv ~/.monsterget/skill ~/.monsterget/skills/tiktok-collector
> ```
> Then update the pointer in your rules file. The tiktok and linkedin runtimes then coexist without conflict.

## 🧠 Architecture (what actually happens)

```
AI ──▶ generates taskId + opens browser URL
         │
Your Browser ──▶ MonsterGet extension runs the scrape in your TikTok/X/LinkedIn/Upwork/app-store tab
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