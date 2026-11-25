# VOC Miner Eval Cases

Run these 3 cases before every release. Each case is a specification; use real
data when available, or a fixed fixture CSV for regression.

## Case 1 — DTC skincare brand (cross-source)

**Input**

```text
Brand: {skincare brand}
Category: acne treatment
App: {App Store URL}
Market: US / EN
Focus: churn + product complaints
```

**Expected behavior**

- Collects TikTok comments from 3–5 top videos, X comments from 3–5 posts,
  App Store reviews (US), Google Play reviews (EN).
- Produces at least 5 themes, including at least one theme with quotes from
  2 different sources.
- Separates "what users love" from "what users complain about".
- Produces 3 action drafts (product, support, marketing).
- Reports Coverage / Cost / Confidence.

**Checks**

- [ ] At least 500 total items (comments + reviews), or confidence = Low.
- [ ] Every theme has >= 3 quotes and >= 2 sources.
- [ ] Quotes are verbatim and linked.
- [ ] No demographic claims.
- [ ] No "guaranteed" claims.
- [ ] Report includes "Data boundary & confidence".

## Case 2 — B2B SaaS mobile app (negative reviews)

**Input**

```text
Brand: {B2B SaaS}
App: {App Store URL}
Market: US / EN
Focus: onboarding, sync failures, pricing confusion
Filter: 1–2 star reviews, last 6 months
```

**Expected behavior**

- Collects 200+ 1–2 star reviews.
- Codes reviews into churn, support, feature request, confusion.
- Identifies the top 3 reasons for negative reviews.
- Drafts 3 support reply templates.
- Notes that 1–2 star reviews are not representative of all users.

**Checks**

- [ ] Star filter is stated in the report.
- [ ] Churn reasons are separated from feature requests.
- [ ] Support templates are empathetic and specific.
- [ ] Confidence is not "High" unless sample >= 300.
- [ ] No claim about "all users".

## Case 3 — Mobile game (version regression)

**Input**

```text
Game: {game}
Platform: Google Play
Market: JP / ZH / EN
Focus: version regression, crashes, monetization complaints
```

**Expected behavior**

- Collects reviews across 2–3 languages.
- Groups complaints by app version when available.
- Flags a version regression if a spike in negative reviews aligns with a version.
- Produces a "what changed" hypothesis, labelled as inference.
- Recommends 3 fixes + 1 monitoring plan.

**Checks**

- [ ] Language distribution is reported.
- [ ] Version regression is labelled as a hypothesis, not fact.
- [ ] No translation of quotes without the original.
- [ ] At least one quote per language (if available).
- [ ] Coverage / Cost / Confidence present.

## Scoring

| Dimension | Weight | Pass criteria |
|---|---:|---|
| Data coverage | 25% | Sources and rows match the plan; missing data is disclosed |
| Theme quality | 25% | Themes are distinct, actionable, evidence-backed |
| Evidence fidelity | 20% | Quotes verbatim, links valid, no invented data |
| Actionability | 15% | Drafts are specific and usable |
| Guardrails | 15% | No demographics, no guarantees, privacy respected |

Pass: >= 80/100. Any invented quote or fabricated number = automatic fail.
