# Getting started (English)

> Goal: install, say one sentence, get your first result. No API key, no coding.

---

## 1. What you need

- An AI client that can install local skills: Claude Code, Codex, Cursor, Cline, Windsurf, Kimi, etc. (desktop / IDE, not a browser chat).
- Chrome or Edge.
- A free MonsterGet account: https://monsterget.com
- The MonsterGet extension: https://monsterget.com/install
- Your own login on the target platform (TikTok / X / LinkedIn / Upwork). App Store and Google Play reviews need **no** store login.

**One rule:** the extension, the monsterget.com login, and the target-site login must all be in the **same browser**.

---

## 2. Install

Minimal:

> Install the tiktok-collector skill from https://github.com/monsterget-com/skills

Swap `tiktok-collector` for `x-collector`, `linkedin-collector`, `upwork-collector`, or `app-reviews-collector`.
For App review reports, also install `app-reviews-analyst`.

Full set:

> Install these skills from https://github.com/monsterget-com/skills:
> tiktok-collector, x-collector, linkedin-collector, upwork-collector,
> app-reviews-collector, app-reviews-analyst, monsterget-context,
> monsterget-business, voc-miner, freelance-lead-radar

Skills are copied to `~/.monsterget/skills/<skill>/`. Re-run the install message to upgrade.

---

## 3. First setup (~3 minutes, once)

1. Install the extension: https://monsterget.com/install
2. Log in to https://monsterget.com
3. Log in to the target site (e.g. https://www.tiktok.com)

All in the same browser, then tell the AI you are ready.
The AI never scans your disk or opens test windows.

---

## 4. Say your first task

Talk about the **decision** and the **subject**, not the scraper.

**App reviews (full report available):**

> Analyze CapCut's 1–2 star reviews on the App Store and Google Play for the last 90 days.
> Give me an HTML report focused on what iOS and Android users complain about differently.

**TikTok content / creators (collection ready):**

> Look at @theordinary's last 100 videos. Give me the CSV, rank the top 10 by engagement,
> and tell me 3 content angles I can reuse.

**Upwork (business skill available):**

> I'm a React frontend dev at $60/hour, remote only. Find Upwork jobs from the last 14 days,
> rank the top 10, and draft a proposal for each.

More prompts: [business menu (zh)](../zh/business-menu.md).

---

## 5. What you get

| File | Purpose |
|---|---|
| `*.csv` | Raw collected data; opens in Excel / Numbers |
| `manifest.json` | What was scraped, how many rows, when |
| `metrics.json` | Every metric used by the report |
| `report.html` | Single-file report; print to PDF from the browser |
| `tables/*.csv` | Rating distribution, themes, daily trend, quotes |

Every number in the report is computed from the CSV; nothing is invented.
Missing fields are shown as "no data" instead of zero.

---

## 6. Quick / Standard / Deep

The first run defaults to a **Quick sample** (3–5 minutes, directional only).
Upgrade to Standard for a report you can put in front of a client.

| Tier | Use | Typical size | Time |
|---|---|---|---|
| Quick | first signal / demo | 50–200 per source | 3–5 min |
| Standard | normal business report | 500–2,000 per source | 8–20 min |
| Deep | competitors / multi-market / high stakes | 2,000–4,000 | 30–60 min |

The AI must say which tier it is using and label a Quick sample as a small sample.

---

## 7. After the first result

You can just say:

- "Only the last 30 days" → usually no re-scrape.
- "Add a competitor" → re-scrape; the AI should report the number of scrapes first.
- "Split by app version" → depends on whether the CSV has a version field.
- "Give me the 20 creators" → export from the table, no re-scrape.
- "Turn it into social cards / a video script" → planned content skills.

Before any extra scrape, the AI should tell you: what, how many rows, how long, what is missing.

---

## 8. When something fails

| Symptom | Check |
|---|---|
| Browser does not open | Is the extension installed in the browser you told the AI? |
| Stuck / `not_found` | Logged in to monsterget.com? Target site? Window visible? |
| 0 rows | Is the URL/keyword correct? Try a broader query. |
| No report | Python 3.10+? CSV columns? Sample below the minimum? |
| Partial data | Coverage says what is missing; do not treat it as the full picture. |

Full FAQ (zh): [常见问题](../zh/faq.md).
