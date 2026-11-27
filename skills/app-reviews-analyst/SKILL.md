---
name: monsterget-app-reviews-analyst
description: >-
  Analyze App Store (iOS) and Google Play (Android) review CSVs into a
  self-contained HTML report, metrics.json, and CSV tables. Use when the user
  wants review insights, dual-store comparison, version/country breakdowns,
  complaint themes, or a report to share. Requires Python 3.10+ (standard
  library only). Pair with monsterget-app-reviews-collector for data collection.
---

# App Reviews Analyst

Turns review CSVs into a **decision-ready report**:

- rating distribution and negative share
- complaint themes (keyword taxonomy, reproducible)
- daily negative trend (3-day moving average)
- anonymized quotes
- `metrics.json` + `tables/*.csv` for downstream skills (XHS cards, video, slides)

> This skill **does not collect data**. If the user has no CSV, run
> `monsterget-app-reviews-collector` first, or accept a CSV they already exported.

## 🌍 Language rule

Always reply to the user in the user's language. The report itself supports
`zh` and `en` via `options.language`.

## When to use

- "分析这个 App 的差评 / 对比 iOS 和安卓 / 哪个版本问题最多"
- "把这两份评论 CSV 做成一份报告"
- "App Store 和 Google Play 的评论有什么不同"
- "给我一份能发给老板/客户的评论分析"

Do **not** use for: collecting reviews, making Xiaohongshu cards/video, or
social-media publishing. Those are separate skills.

## Inputs

1. **CSV files** from `monsterget-app-reviews-collector` (App Store and/or Google Play).
   Required columns: `评分` (or `rating`), `正文` (or `text`), `时间` (or `date`).
   Optional: `平台`, `国家`, `语言`, `版本`, `评论ID`, `点赞数`.
2. **A job JSON** describing datasets, filters, sampling, and output.

CSV must be UTF-8 (BOM ok). One file per store is recommended; the analyst
merges them and segments by `platform`.

## Output

```
runs/<run_id>/
  manifest.json      # run contract for downstream content skills
  metrics.json       # all metrics, sample, quality, taxonomy version
  report.html        # single file, inline CSS/SVG, print to PDF
  tables/
    rating_distribution.csv
    theme_share.csv
    daily.csv
    quotes.csv
  quality.json       # only when the run is rejected
```

`metrics.json` and `manifest.json` are the handoff contract. Downstream skills
must read them instead of recomputing numbers.

## Quick start

```bash
python3 scripts/run.py --job job.json
```

Minimal job:

```json
{
  "run_id": "capcut-dual-2026-11",
  "out": "runs/capcut-dual-2026-11",
  "recipe": "dual_store",
  "datasets": [
    {"name": "ios", "path": "/path/ios.csv", "platform": "iOS"},
    {"name": "android", "path": "/path/android.csv", "platform": "Android"}
  ],
  "options": {
    "rating_max": 2,
    "date_range": ["2026-11-07", "2026-11-26"],
    "sample_per_segment": 500,
    "sample_seed": 42,
    "taxonomy": "app_reviews",
    "language": "zh",
    "top_quotes": 2,
    "min_rows": 50
  }
}
```

Notes:

- `date_range` is start-inclusive, end-exclusive. A date-only end is treated as
  the next day 00:00 UTC, so `2026-11-26` includes Nov 25.
- `sample_per_segment` is optional. If set, each segment is randomly sampled
  deterministically with `sample_seed`; the report records original / filtered /
  final counts.
- `min_rows` guards against reporting on tiny samples. Lower it only for a
  deliberate small-sample test.

## What the report contains

1. Executive summary — negative share, shared theme, biggest segment gap.
2. Sample & method — rows, date range, countries, versions, sampling.
3. Rating distribution — 1–5★ stacked bars.
4. Negative themes — per-segment share table with bars.
5. Daily negative rate — 3-day moving average.
6. Quotes — anonymized, grouped by segment and theme.
7. Data-based actions — clearly labeled as suggestions, not causal claims.
8. Limitations — public sample, keyword taxonomy, time-window caveats, PII.

## Guardrails

- **No PII in the report.** Quotes are scrubbed for emails, URLs, @handles, and
  phone numbers. The report never shows usernames or avatars.
- **No invented numbers.** Every metric is computed from the CSV; the narrative
  is template-based in v1.
- **No causal claims.** Say "associated with", not "caused by".
- **Label the sample.** Always include rows, date range, locale, and filters.
- **Do not compare raw counts across platforms.** Compare shares within each
  segment.
- **No private data.** Only public reviews; do not attempt to enrich identities.

## Extending

- Add a taxonomy JSON under `taxonomies/`; no code change.
- Add options (e.g., `segments: ["country"]`) by extending `metrics.py`; keep
  `analysis_schema` versioned.
- Downstream content skills (XHS cards, video) must read `metrics.json` and
  `manifest.json`; they must not import this skill's internals.
