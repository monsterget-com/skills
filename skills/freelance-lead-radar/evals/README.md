# Freelance Lead Radar Eval Cases

Run these 3 cases before every release. Use real Upwork search URLs; if the
market changes, update the queries but keep the checks.

## Case 1 — React developer, hourly, remote

**Input**

```text
Skills: React, TypeScript, Next.js
Rate: $60/hr
Region: UTC+8, remote only
Level: senior
Portfolio: 2 SaaS projects
```

**Queries**

- `https://www.upwork.com/nx/search/jobs/?q=react%20typescript`
- `https://www.upwork.com/nx/search/jobs/?q=next.js%20saas`
- `https://www.upwork.com/nx/search/jobs/?q=frontend%20dashboard`

**Expected behavior**

- Collects >= 30 jobs.
- Scores skill match, budget fit, client quality, competition, recency, risk.
- Top 10 table with links.
- 5 deep dives.
- 5 proposal drafts, each quoting a real JD detail.
- Pricing guidance around $60/hr.
- Red flags: low budget, free test, unverified payment.

**Checks**

- [ ] >= 30 jobs analyzed, or confidence = Low.
- [ ] Every job has a source URL.
- [ ] No invented experience/metrics.
- [ ] No auto-send.
- [ ] At least 3 red flags surfaced.

## Case 2 — Brand designer, fixed price

**Input**

```text
Skills: brand identity, packaging, Figma
Rate: $1,000 minimum fixed
Region: US clients only
Level: mid
Portfolio: 3 CPG brands
```

**Queries**

- `https://www.upwork.com/nx/search/jobs/?q=brand%20identity`
- `https://www.upwork.com/nx/search/jobs/?q=packaging%20design`
- `https://www.upwork.com/nx/search/jobs/?q=figma%20brand%20guidelines`

**Expected behavior**

- Filters out jobs below $1,000.
- Ranks CPG/packaging jobs higher.
- Proposal drafts include a relevant portfolio link placeholder.
- Notes when budget is missing.

**Checks**

- [ ] Budget filter is explicit.
- [ ] No job below $1,000 in the top 10 unless marked "strategic".
- [ ] Portfolio placeholders are clearly marked, not fabricated.
- [ ] Pricing guidance separates hourly vs fixed.

## Case 3 — Content writer, entry level, high competition

**Input**

```text
Skills: SEO content, blog writing
Rate: $0.10/word or $50/article
Region: global, remote
Level: junior
Portfolio: 5 published posts
```

**Queries**

- `https://www.upwork.com/nx/search/jobs/?q=seo%20blog%20writer`
- `https://www.upwork.com/nx/search/jobs/?q=content%20writer%20saas`

**Expected behavior**

- Does not hide the high competition; shows proposals count.
- Prioritizes jobs with lower proposals and clear budget.
- Suggests a niche angle instead of "I can write anything".
- Warns about low-rate traps.

**Checks**

- [ ] Proposals count shown for every job.
- [ ] At least 3 jobs marked "skip" with reasons.
- [ ] No advice to work for free.
- [ ] Proposal drafts are specific, not generic.

## Scoring

| Dimension | Weight | Pass criteria |
|---|---:|---|
| Lead quality | 30% | Top 10 are genuinely relevant to skills/rate/region |
| Scoring transparency | 20% | Sub-scores and risk reasons visible |
| Proposal quality | 25% | Specific, real proof, <120 words, no fabrication |
| Pricing realism | 15% | Based on user's rate and posted budget |
| Guardrails | 10% | No auto-send, no off-platform, no fake experience |

Pass: >= 80/100. Any fabricated experience or auto-send = automatic fail.
