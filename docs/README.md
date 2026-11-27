# MonsterGet 用户文档

> 面向普通用户：第一次用、想知道"能做什么、怎么说、拿到什么、怎么继续"。
> Agent / 开发文档不在这个目录，见文末的"文档分层"。

**如果你只读一篇 → [5 分钟上手](zh/getting-started.md)**

---

## 推荐阅读顺序

| 顺序 | 文档 | 解决什么问题 |
|---:|---|---|
| 1 | [5 分钟上手](zh/getting-started.md) | 装什么、说什么、第一次能拿到什么 |
| 2 | [业务菜单](zh/business-menu.md) | 9 类业务分别要什么输入、给什么结果、现在能不能做 |
| 3 | [报告怎么读](zh/reading-reports.md) | 覆盖率、置信度、主题表、原话怎么用 |
| 4 | [数据与隐私](zh/data-and-privacy.md) | 数据从哪来、存哪里、哪些不做 |
| 5 | [常见问题](zh/faq.md) | Quick/Standard 区别、失败排查、能力边界 |

English quickstart: [Getting started](en/getting-started.md).

---

## 文档分层（很重要）

| 你是谁 | 读什么 | 不要读什么 |
|---|---|---|
| 普通用户 | 本目录、各 skill 的 `INSTALL.md`、真实案例 | `SKILL.md`、`AGENTS.md`、`evals/` |
| 想让 AI 安装 / 执行 | 把仓库链接丢给 AI；AI 自己读 `SKILL.md` / `AGENTS.md` | 不需要你手动读 |
| 开发者 / 贡献者 | `AGENTS.md`、`CATALOG.md`、`DATA-STANDARDS.md`、`scripts/`、`evals/` | 本目录是用户向，不是实现说明 |

> 为什么 `SKILL.md` 很长？它是写给 AI 执行的说明书，不是教程。用户只需要说目标。

---

## 现有真实案例

- [TikTok 竞品分析](../skills/tiktok-collector/case-studies/01-competitor-analysis.md)
- [达人挖掘：两步漏斗](../skills/tiktok-collector/case-studies/02-creator-discovery.md)
- [粉丝数是最大的谎言](../skills/tiktok-collector/case-studies/03-fake-follower-exposed.md)

每个案例都包含：对 AI 说的原话、实际 CSV 预览、分析过程和结论。

---

## 规划中的教程

这些会在对应 skill 发布时补齐，不提前承诺：

- App 双端差评复盘：从两份 CSV 到 `report.html`
- TikTok 品牌运营体检：内容节奏、爆款率、达人候选
- X 舆情 24 小时：关键词 → 时间线 → 证据
- 人才地图 / 岗位市场：LinkedIn 岗位与画像
- 自由职业接单：Upwork 筛选 + proposal 草稿
- 报告迭代：不重抓 vs 补抓，怎么判断
- 常见失败排查：扩展、登录、空数据、窗口被遮挡

---

## 维护约定

- 用户文档只写"用户看得到的东西"：目标、输入、产出、时间、限制。
- 不写 bash、API endpoint、taskId、轮询逻辑、`state.json`、版本号。
- 所有数字必须能回溯到 CSV / `metrics.json`；示例数据要脱敏。
- 能力边界如实标：✅ 一键报告 / 🟡 可取数、需 AI 手工分析 / ⬜ 规划中。
