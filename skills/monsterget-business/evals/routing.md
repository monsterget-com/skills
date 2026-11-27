# Routing Eval — 20 Utterances

Expected: the router picks the primary skill in the right column. If ambiguous,
it should ask at most 1–2 questions, then pick.

| # | User utterance | Expected skill |
|---:|---|---|
| 1 | 帮我分析一下这个品牌在 TikTok 和 App Store 上的用户抱怨 | `voc-miner` |
| 2 | 我想知道用户为什么给我们打一星 | `voc-miner` |
| 3 | 这个品类有什么未被满足的需求？ | `voc-miner` |
| 4 | 帮我看这 3 条视频的评论，提炼产品改进点 | `voc-miner` |
| 5 | Find the top churn reasons for this app from reviews | `voc-miner` |
| 6 | 帮我找 10 个适合我们护肤品牌的 TikTok 达人 | `creator-due-diligence` |
| 7 | 这个达人有没有刷量/翻车风险？ | `creator-due-diligence` |
| 8 | 对比一下这三个竞品最近 30 天的内容 | `competitor-teardown` |
| 9 | 竞品在押什么主题？我们该测什么？ | `competitor-teardown` |
| 10 | 这家公司最近在招什么岗位？给我一张人才地图 | `talent-map` |
| 11 | 我们想从竞争对手那里挖一个数据团队，人才在哪？ | `talent-map` |
| 12 | 我们 App 评分最近掉了，帮我看看版本有没有回归 | `aso-pulse` |
| 13 | 帮我们写一版 App Store 的卖点文案 | `aso-pulse` |
| 14 | 今天 Upwork 上最值得投的 10 个单 | `freelance-lead-radar` |
| 15 | 帮我把这个 Upwork JD 写成 proposal | `freelance-lead-radar` |
| 16 | 诊断一下我的 TikTok 账号，为什么最近播放掉了 | `creator-growth-audit` |
| 17 | 我的账号适合做什么内容？ | `creator-growth-audit` |
| 18 | 我想投这个 LinkedIn 岗位，帮我分析匹配度和面试准备 | `job-fit-coach` |
| 19 | 帮我看看这份 JD 和我的简历差在哪 | `job-fit-coach` |
| 20 | 我想做用户研究，但不知道从哪开始 | `monsterget-context` first, then ask |

## Pass criteria

- ≥ 18/20 correct primary skill.
- No more than 2 clarifying questions per ambiguous case.
- Never route a private-data request to a collector; explain the limit.
- Never route "auto-apply / auto-send" to a business skill; refuse the automation
  part and offer drafts.

## Ambiguity rules

- "分析一下这个品牌" → ask: "你想看用户抱怨（VOC）、竞品内容，还是达人合作？"
- "帮我做增长" → ask: "你想先做内容、达人，还是用户研究？"
- "看看这个市场" → ask: "你是要市场进入、竞品拆解，还是人才地图？"
- "帮我写报告" → ask: "报告的主题是什么？用户、竞品、达人，还是招聘？"
