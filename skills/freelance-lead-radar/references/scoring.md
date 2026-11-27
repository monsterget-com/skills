# Lead Scoring Rubric

All sub-scores are 0–100. The final `fit_score` is 0–100 after the risk penalty.

```text
fit_score =
  skill_match * 0.30 +
  budget_fit * 0.20 +
  client_quality * 0.20 +
  competition * 0.15 +
  recency * 0.10 +
  risk_penalty
```

## 1. Skill match (30%)

| Score | Criteria |
|---:|---|
| 90–100 | Core skills + domain match; user has direct proof |
| 70–89 | Core skills match; domain adjacent |
| 50–69 | Partial match; learnable gap |
| 30–49 | Stretch; significant gap |
| 0–29 | Wrong skill set |

Signals: JD keywords, required skills, deliverables, industry, tooling.

## 2. Budget fit (20%)

| Score | Criteria |
|---:|---|
| 90–100 | At or above the user's target rate; budget clearly stated |
| 70–89 | 10–20% below target but scope is smaller |
| 50–69 | 20–35% below target; negotiable |
| 30–49 | Far below target; only worth it for portfolio/strategy |
| 0–29 | Insulting/low-ball; walk away |

If the budget is missing, score 50 and mark "budget unknown".

## 3. Client quality (20%)

| Score | Criteria |
|---:|---|
| 90–100 | Payment verified, high spend, good rating, high hire rate |
| 70–89 | Verified, some history, decent rating |
| 50–69 | New client or limited history |
| 30–49 | Unverified payment or mixed reviews |
| 0–29 | Poor history, disputes, or clear red flags |

Signals: payment verification, total spend, rating, hire rate, reviews, country.

## 4. Competition (15%)

| Score | Criteria |
|---:|---|
| 90–100 | Few proposals relative to budget; niche skill |
| 70–89 | Below-average proposals |
| 50–69 | Average |
| 30–49 | Many proposals |
| 0–29 | 50+ proposals for a small budget |

If proposals are unknown, score 50.

## 5. Recency (10%)

| Score | Criteria |
|---:|---|
| 100 | Posted within 24h |
| 80 | 1–3 days |
| 60 | 4–7 days |
| 40 | 8–14 days |
| 20 | 15–30 days |
| 0 | Older than 30 days |

## 6. Risk penalty (0 to -40)

Subtract:

| Risk | Penalty |
|---|---:|
| Budget far below rate | -15 |
| Asks for free test / spec work | -15 |
| Payment unverified | -10 |
| Vague scope / copy-pasted JD | -10 |
| Many proposals + low budget | -10 |
| Off-platform contact request | -10 |
| Unrealistic deadline | -5 |
| "Simple task" with huge scope | -10 |
| Client history of disputes | -15 |

Cap the total penalty at -40. Always show the reasons in the table.

## 7. Decision bands

| Fit score | Action |
|---:|---|
| 80–100 | Apply today; tailor proposal |
| 65–79 | Apply if capacity; tailor lightly |
| 50–64 | Only if strategic (portfolio, long-term) |
| < 50 | Skip |

## 8. Pricing guidance

- Use the user's target rate as the anchor.
- If the client's budget is below target but the scope is smaller, propose a
  reduced scope at the target rate.
- If the client has a strong history and long-term potential, offer a small
  discount (max 15%) with a clear reason.
- Never recommend working for free or "just to get a review".
- Do not invent market rates; if unknown, say "based on your target rate and the
  budget in the post".

## 9. Proposal angle selection

| Job signal | Angle |
|---|---|
| Clear pain / broken process | "Here's how I'd fix X first" |
| New product / MVP | "Smallest path to launch" |
| Existing team overload | "I can take X off your plate" |
| Design-heavy | "Show a relevant before/after" |
| Data/analytics | "Here's the metric I'd move" |
| Retainer/long-term | "30-day plan" |

Keep the opener specific to the JD. No generic praise.
