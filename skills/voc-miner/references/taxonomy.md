# VOC Coding Taxonomy

Use this taxonomy to code comments and reviews consistently. A single item can
carry more than one code. Preserve the original wording; do not paraphrase quotes.

## 1. Codes

| Code | What it means | Example signals |
|---|---|---|
| `question` | The user asks how something works, whether it supports X, or what to do | "does it work with…", "how do I…", "can I…" |
| `objection` | Doubt, fear, or reason not to buy/use | "too expensive", "won't work for…", "I don't trust…" |
| `pain` | A frustration, failure, or unmet need | "crashes when…", "takes forever", "support never replies" |
| `desired_outcome` | What the user wants to achieve | "I just want…", "ideally it would…" |
| `buying_intent` | Explicit interest in buying/using | "where can I get", "link?", "how much", "DM me" |
| `praise` | Specific thing that worked | "the onboarding was smooth", "love the export" |
| `feature_request` | A concrete new capability | "please add…", "would be great if…" |
| `confusion` | Misunderstanding of what the product does | "wait, is this for…?", "I thought it was…" |
| `churn` | Cancel, refund, switch, or stop using | "cancelled", "switched to…", "refund" |
| `support` | Support, logistics, billing, delivery, warranty | "no reply", "wrong item", "charged twice" |
| `competitor` | Mentions an alternative | "unlike X", "switched from Y" |

## 2. Coding rules

1. **Code the user's meaning, not keywords.** "This is sick" can be praise or
   disgust; read the context.
2. **One item can have multiple codes.** A complaint can also contain a feature
   request and a competitor mention.
3. **Do not code spam, bots, emoji-only, or the brand's own replies** as VOC.
4. **Keep the exact quote.** Fix typos only in a separate `quote_clean` field, never
   in `quote`.
5. **Do not infer demographics.** No age, gender, income, ethnicity, or health
   claims unless the user explicitly stated it and it is necessary.
6. **Separate observation from inference.** Mark inferred themes as "appears to".
7. **Respect the source.** A comment on a viral video is not representative of the
   whole market; say so.

## 3. Severity

Use a simple, explainable score (0–100):

```text
severity = negative_weight × frequency_share × intensity
```

| Factor | Values |
|---|---|
| `negative_weight` | 1-star = 1.0, 2-star = 0.8, 3-star = 0.5, 4-star = 0.2, 5-star = 0.1; comments with explicit churn/refund = 1.0 |
| `frequency_share` | theme_count / total_items |
| `intensity` | 1.0 if strong emotion or repeated failure, 0.7 if matter-of-fact, 0.4 if mild |

Round to 1 decimal. Always show the inputs in `themes.csv`.

## 4. Theme aggregation

A theme is valid only if:

- at least **3 quotes**
- at least **2 sources** (e.g., 2 videos, or TikTok + App Store)
- a clear one-sentence definition
- a count and a severity score

If a theme has 1–2 quotes, put it under "Weak signals" and label confidence low.

## 5. Quote selection

For each theme, pick quotes that are:

1. **Representative** of the theme, not just the most extreme.
2. **Specific** (mentions the feature, flow, or outcome).
3. **Diverse** (different authors/sources when possible).
4. **Verbatim** and linked.

Prefer quotes with higher likes only when they are also representative.

## 6. Output fields for `quotes.csv`

```csv
quote_id,theme,code,quote,quote_clean,platform,source_url,author_handle,likes,published_at,rating,country,lang
```

## 7. Output fields for `themes.csv`

```csv
theme,type,frequency,sample_size,share,severity,negative_weight,intensity,source_count,quote_count,confidence,definition
```

## 8. Confidence

| Sample size | Confidence |
|---|---|
| < 30 comments or < 100 reviews | Low |
| 30–99 comments or 100–299 reviews | Medium |
| >= 100 comments or >= 300 reviews | High |

Also downgrade one level if:

- only one source
- the source is a single viral post
- the query is narrow
- the data is older than 90 days
