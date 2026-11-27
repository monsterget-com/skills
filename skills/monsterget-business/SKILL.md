---
name: monsterget-business
description: >-
  Use when the user asks a business question that needs public data research:
  VOC, 用户之声, 评论分析, 差评分析, 产品需求, 竞品分析, 达人筛选, 达人背调,
  influencer vetting, 人才地图, 招聘情报, talent mapping, ASO, app review
  analysis, 自由职业接单, Upwork leads, 账号诊断, 求职匹配, or "我该用哪个
  skill". Reads `.agents/monsterget-context.md`, picks the right MonsterGet
  business skill, estimates data volume/time, and confirms before running.
allowed-tools: Read, Write, Bash
version: 2.0.0
metadata:
  monsterget:
    category: router
    requires:
      skills: [monsterget-context]
    outputs: ["selected skill + data plan + estimate"]
    related: [voc-miner, creator-due-diligence, competitor-teardown, talent-map, aso-pulse, freelance-lead-radar, creator-growth-audit, job-fit-coach]
---

# MonsterGet Business Router

One entry point for all MonsterGet business skills. The user should not have to
know which skill to install.

## Step 0 — Load context

1. Read `.agents/monsterget-context.md`.
2. If missing, run `monsterget-context` first, or use a lightweight context:
   - business name
   - product/category
   - target customer
   - market/language
   Say confidence will be lower.

## Step 1 — Classify the request

Use the routing table. Pick exactly one primary skill. If two apply, pick the one
closest to the user's **decision**, not the data source.

| User intent | Primary skill |
|---|---|
| 用户抱怨 / 差评 / 产品需求 / 评论分析 / VOC / voice of customer / churn reasons | `voc-miner` |
| 达人 / 网红 / 合作 / 带货 / 背调 / influencer vetting / creator sourcing | `creator-due-diligence` |
| 竞品 / 对标 / 内容策略 / 爆款 / competitor content / outlier | `competitor-teardown` |
| 招聘 / 人才地图 / 目标公司 / HR / talent map / org chart | `talent-map` |
| App 评论 / ASO / 评分 / 版本回归 / app review analysis | `aso-pulse` |
| Upwork / 接单 / 自由职业 / proposal / freelance leads | `freelance-lead-radar` |
| 我的账号 / 涨粉 / 诊断 / my account audit | `creator-growth-audit` |
| 求职 / 面试 / 岗位匹配 / job fit / interview prep | `job-fit-coach` |

## Step 2 — Ask only if ambiguous

Ask at most 1–2 questions:

- "你想支持的决策是什么：选达人、改产品、做内容、还是找工作？"
- "你有具体品牌/账号/岗位链接吗？没有的话我先帮你找候选。"
- "你要英文还是中文输出？"

Do not interrogate. If the user is vague, pick the most likely skill and say
"我先按 X 做，如果你要的是 Y，告诉我。"

## Step 3 — Build the data plan and estimate

Before running, show a small plan:

```text
Skill: voc-miner
Data:
  - TikTok comments: 3 videos × 100 = 300
  - X comments: 3 posts × 100 = 300
  - App Store reviews: 500 (if app URL provided)
  - Google Play reviews: 500 (if package provided)
Login needed: tiktok.com, x.com
Estimated: 4–6 scrapes, 3–8 minutes
Output: VOC report + themes.csv + quotes.csv + action drafts
```

Rules:
- Estimate rows and scrapes, not fake precision.
- If > 10 scrapes, ask for confirmation.
- If a required platform is not installed, say which collector to install.
- If a required login is missing, say which site to log in to.

## Step 4 — Confirm

Ask one short question: "按这个计划跑？" If yes, load the chosen skill and follow
its workflow. If no, adjust.

## Step 5 — Hand off

When loading the chosen skill:

1. Tell the user which skill you are using, in plain language.
2. Pass the context file path and the data plan.
3. Follow the chosen skill's Output Format and Quality Gates.
4. At the end, report Coverage / Cost / Confidence.

## Coverage / Cost / Confidence contract

Every routed task must end with:

```text
Coverage: {rows} rows from {n} sources; missing: {what}
Cost: {scrapes} scrapes, ~{time}, {retries} retries
Confidence: High / Medium / Low ({reason})
```

## What NOT to do

- Do not run a skill without context unless the user refuses.
- Do not run more than ~10 scrapes without asking.
- Do not promise private data, demographics, transcripts, or ad libraries.
- Do not auto-send outreach; drafts only.
- Do not mix enterprise and personal tone; ask which output the user wants.
- Do not hide partial coverage.

## Related skills

- `monsterget-context` — must run first.
- All business skills listed above.
- Collector skills: install only the platforms needed.
