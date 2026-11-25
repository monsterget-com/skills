# VOC Report Template

```markdown
# VOC Report: {brand / product}

**Coverage:** {n} comments + {n} reviews from {sources}; missing: {what}
**Cost:** {scrapes} scrapes, ~{time}, {retries} retries
**Confidence:** High / Medium / Low ({reason})

## One-line verdict

{One sentence a product lead can repeat in a meeting.}

## Top 3 findings

1. **{Theme}** — {frequency} mentions, severity {score}. Evidence: "{quote}"
   ([source]({url}))
2. **{Theme}** — ...
3. **{Theme}** — ...

## Themes

| Theme | Type | Frequency | Share | Severity | Representative quote | Sources |
|---|---|---:|---:|---:|---|---|
| {theme} | {code} | {n} | {%} | {score} | "{quote}" | [1]({url}), [2]({url}) |

## What users love

- **{Theme}** — {n} mentions. "{quote}" ([source]({url}))
- ...

## What users complain about

- **{Theme}** — {n} mentions, severity {score}. "{quote}" ([source]({url}))
  - Likely cause: {inference, labelled}
  - Evidence: {n} quotes across {n} sources

## What users want (feature requests)

| Request | Mentions | Evidence | Why it matters |
|---|---:|---|---|
| {request} | {n} | "{quote}" ([source]({url})) | {impact} |

## Why users leave (churn)

| Reason | Mentions | Evidence | Save play |
|---|---:|---|---|
| {reason} | {n} | "{quote}" ([source]({url})) | {draft} |

## Competitor mentions

| Competitor | Context | Sentiment | Evidence |
|---|---|---|---|
| {name} | {context} | positive/negative/mixed | "{quote}" ([source]({url})) |

## Exact language to reuse

### For copy / ads
- "{quote}"
- "{quote}"

### For support macros
- "{quote}"
- "{quote}"

### For product docs
- "{quote}"

## Action drafts

### Product (top 3)
1. **{Change}** — evidence: {theme}, {n} mentions. Expected impact: {impact}.
2. ...
3. ...

### Support (top 3 reply templates)
1. **{Complaint}** — template:
   > "{reply}"
2. ...

### Marketing (top 3 angles)
1. **{Angle}** — based on "{quote}". Suggested hook: "{hook}".
2. ...

## Data boundary & confidence

- Platforms: {platforms}
- Query / URLs: {queries}
- Date range: {range}
- Sample: {n} comments + {n} reviews
- Missing: {what}
- Limitations: public sample only; not representative of all users; no demographic
  inference; sentiment is directional.
- Confidence: {High/Medium/Low} because {reason}.

## Method

1. Collected public comments/reviews from {sources}.
2. Deduplicated spam and brand replies.
3. Coded each item into the VOC taxonomy.
4. Clustered into themes with >= 3 quotes and >= 2 sources.
5. Computed frequency and severity with the published formula.
6. Selected representative verbatim quotes.
```

## Notes for the writer

- Never invent a quote, number, or source.
- If a theme has fewer than 3 quotes, move it to "Weak signals" and lower
  confidence; do not present it as a top finding.
- Keep quotes in their original language; translate only in a separate line.
- Do not include personal data beyond a public handle.
