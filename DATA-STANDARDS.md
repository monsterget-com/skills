# MonsterGet Data Standards

Every business skill must state **how much data it needs** before it starts.
"Enough" is not a feeling; it is a tier + a per-source quota + a confidence rule.

This file is the shared baseline. Individual skills can be stricter, but not weaker.

---

## 1. Three tiers

| Tier | Use when | What the user gets | Typical time |
|---|---|---|---|
| **Quick** | demo, smoke test, first look | directional signal; low/medium confidence | 5–10 min |
| **Standard** | normal client report | defensible themes; medium/high confidence | 20–40 min |
| **Deep** | high-stakes decision, enterprise, investment | saturation-checked; high confidence | 45–90 min |

**Rule:** if the user does not specify, default to **Standard**. Do not silently run Quick.

---

## 2. Per-skill standards

### VOC Miner

| Tier | Posts/videos | Comments | App reviews | Total analyzed | Scrapes |
|---|---:|---:|---:|---:|---:|
| Quick | 3–5 | 100–200 | 100–200 | 200–400 | 3–5 |
| **Standard** | 5–8 | 500–1,000 | 500–1,000 | **1,000–2,000** | 8–12 |
| Deep | 8–12 | 1,500–2,000 | 1,500–2,000 | 3,000–4,000 | 15–20 |

**Minimum for a report:** 300 comments **or** 500 reviews, from **>= 2 sources**.
Below that → label `Low` confidence and say "directional".

**Saturation:** collect in batches of ~100 comments. Stop when **2 consecutive
batches add < 10% new themes**. If not saturated by the tier cap, say so.

### Creator Due Diligence

| Tier | Creators | Posts per creator | Comments per creator | Total posts |
|---|---:|---:|---:|---:|
| Quick | 5 | 20 | 50 | 100 |
| **Standard** | 10–20 | 30–50 | 100 | 300–1,000 |
| Deep | 20–30 | 50 | 100–200 | 1,000–1,500 |

**Minimum:** 10 creators × 20 recent posts. Fewer → `Low` confidence.

### Competitor Teardown

| Tier | Competitors | Posts per competitor | Total posts |
|---|---:|---:|---:|
| Quick | 3 | 30 | 90 |
| **Standard** | 5 | 50–100 | 250–500 |
| Deep | 8 | 100 | 800 |

**Minimum:** 3 competitors × 30 posts.

### Freelance Lead Radar

| Tier | Queries | Unique jobs | Proposals drafted | Scrapes |
|---|---:|---:|---:|---:|
| Quick | 1–2 | 30–50 | 3 | 2–3 |
| **Standard** | 3–5 | 100–200 | 10 | 5–8 |
| Deep | 5–8 | 300–500 | 10–20 | 10–15 |

**Minimum:** 50 unique jobs posted in the last 14 days. Fewer → `Low` confidence.

### ASO Pulse

| Tier | Reviews per store | Stores | Total reviews |
|---|---:|---:|---:|
| Quick | 200 | 1 | 200 |
| **Standard** | 500–1,000 | 2 | 1,000–2,000 |
| Deep | 2,000 | 2 | 4,000 |

**Minimum:** 300 reviews. Below that → `Low` confidence.

### Talent Map

| Tier | Companies | People per company | Total people |
|---|---:|---:|---:|
| Quick | 5 | 20 | 100 |
| **Standard** | 10–15 | 20–50 | 200–750 |
| Deep | 20 | 50 | 1,000 |

**Minimum:** 5 companies × 20 people.

### Job Fit Coach

| Tier | Jobs compared | Detail pages | Prep depth |
|---|---:|---:|---|
| Quick | 5 | 1 | short |
| **Standard** | 20–30 | 3–5 | full |
| Deep | 50+ | 10 | full + outreach |

### Creator Growth Audit

| Tier | Own posts | Competitor posts | Comments |
|---|---:|---:|---:|
| Quick | 30 | 0 | 0 |
| **Standard** | 50–100 | 3 × 30 | 100 |
| Deep | 200 | 5 × 50 | 500 |

---

## 3. Counting rules

1. **Count unique items after dedupe.** Raw CSV rows are not the sample.
2. **Subtract spam, bots, emoji-only, and the brand's own replies.**
3. **Per-source quota:** no single source may exceed **70%** of the analyzed
   sample. If it does, add another source or lower confidence.
4. **Recency:**
   - content / creators: last **30–90 days**
   - app reviews: last **6–12 months**
   - jobs: last **14 days** (7 for daily radar)
5. **Oversample 10–20%** to account for dedupe and failures.
6. **Log the query plan** (queries, pages, counts, dates) in the report.
7. **If a collector returns fewer than requested**, do not pretend it hit the
   target. Try another query angle/page, then report the actual count.
8. **Never count a 0-row or failed scrape** toward the sample.

---

## 4. Confidence rules

### VOC

| Analyzed items | Confidence |
|---|---|
| < 300 comments or < 500 reviews | Low |
| 300–999 comments or 500–1,499 reviews | Medium |
| >= 1,000 comments or >= 1,500 reviews | High |

Downgrade one level if: only one source, one viral post, a narrow query, or data
older than 90 days.

### Freelance

| Unique jobs | Confidence |
|---|---|
| < 50 | Low |
| 50–149 | Medium |
| >= 150 | High |

### Creator DD / Competitor

| Creators / competitors | Confidence |
|---|---|
| < 10 creators or < 3 competitors | Low |
| 10–19 creators or 3–4 competitors | Medium |
| >= 20 creators or >= 5 competitors | High |

### ASO

| Reviews | Confidence |
|---|---|
| < 300 | Low |
| 300–999 | Medium |
| >= 1,000 | High |

---

## 5. Collector caps (hard limits)

| Scraper | Per call max | Default | Notes |
|---|---:|---:|---|
| `tiktok_search_video` | 300 | 50 | one query may return less; use multiple query angles |
| `tiktok_search_user` | 300 | 30 | |
| `tiktok_user_videos` | 300 | 50 | |
| `tiktok_tag` | 300 | 30 | |
| `tiktok_comments` | 200 | 50 | per video; replies optional |
| `x_search_timeline` | 100 | 50 | per query |
| `x_tweet_comments` | 1,000 | 200 | per tweet |
| `app_store_reviews` | 10,000 | 500 | per country |
| `google_play_reviews` | 5,000 | 500 | per language |
| `upwork_search_jobs` | 50/page | 10 | `pages` 1–100 or 0 = auto |
| `linkedin_search_jobs` | 25/page | 25 | `pages` 1–50 or 0 = auto |
| `linkedin_search_people` | 10/page | 10 | `pages` 1–50 |
| `linkedin_profile_main` | 1/URL | 1 | batch up to 50 URLs |
| `linkedin_job_detail` | batch | — | paste job URLs |

**If the target exceeds a cap, the skill must use multiple queries/pages and say
so in the report.** Do not ask the collector to exceed its max.

---

## 6. How to put this in a skill

Add this block to every business `SKILL.md`:

```markdown
## Data volume standard

Default: **Standard**. See [DATA-STANDARDS.md](../../DATA-STANDARDS.md).

| Tier | {source 1} | {source 2} | Total | Scrapes | Time |
|---|---:|---:|---:|---:|---:|
| Quick | ... | ... | ... | ... | ... |
| Standard | ... | ... | ... | ... | ... |
| Deep | ... | ... | ... | ... | ... |

Minimum for a report: ...
Confidence: ...
Saturation: ...
```

Then make the workflow use the tier, and put the actual counts in the report's
Coverage line.

---

## 7. The one-sentence rule

> **A report must say how many unique items it analyzed, from which sources, in
> which date range, and why that is enough for the decision.**
