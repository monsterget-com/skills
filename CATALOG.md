# MonsterGet Skills Catalog

> 这是 v2 的目录文件。它同时给人看，也给 agent 看。
>
> 规则：**先读 `monsterget-context`，再用 `monsterget-business` 选 Skill，最后执行具体 Skill。**

## 0. Data volume standard

Every business skill defaults to **Standard** unless the user asks for Quick
(demo) or Deep (high-stakes):

| Tier | Use when | Typical total |
|---|---|---|
| Quick | demo / smoke test | 200–400 items |
| **Standard** | normal client report | **1,000–2,000 items** |
| Deep | enterprise / investment | 3,000–4,000 items |

See [DATA-STANDARDS.md](DATA-STANDARDS.md) for per-skill quotas, collector caps,
counting rules, saturation and confidence. A report must state how many unique
items it analyzed, from which sources, in which date range, and why that is enough.

## 0. Start here

```text
第一次用？
  1. 安装 collector（按平台）
  2. 运行 monsterget-context，建立品牌/产品/ICP 背景
  3. 运行 monsterget-business，说出你的业务问题
  4. 它会选一个业务 Skill，并告诉你需要多少数据、多久
```

## 1. Collectors（数据层）

| Skill | Platform | Types | 安装 |
|---|---|---:|---|
| `tiktok-collector` | TikTok | 7 | “Install tiktok-collector from monsterget-com/skills” |
| `x-collector` | X/Twitter | 7 | “Install x-collector from monsterget-com/skills” |
| `linkedin-collector` | LinkedIn | 5 | “Install linkedin-collector from monsterget-com/skills” |
| `upwork-collector` | Upwork | 1 | “Install upwork-collector from monsterget-com/skills” |
| `app-reviews-collector` | App Store + Google Play | 2 | “Install app-reviews-collector from monsterget-com/skills” |

> 合计 **22 个 Agent API 爬虫**（`scrapers_api` v4）。另有 2 个 devOnly 未暴露：LinkedIn 公司员工、LinkedIn 档案批量。
>
> Collectors 只负责取数，不做业务分析。它们共用 `run-scrape.sh` 协议和 `~/.monsterget/state.json`。

## 2. Foundation（上下文层）

| Skill | 作用 | 输出 |
|---|---|---|
| `monsterget-context` | 建立/读取品牌、产品、ICP、受众、语气、禁区 | `.agents/monsterget-context.md` |

## 3. Router（路由层）

| Skill | 作用 | 输出 |
|---|---|---|
| `monsterget-business` | 根据用户意图选业务 Skill，估算数据量/时间，确认后执行 | 选中的 Skill + 数据计划 + 预估 |

## 4. Business Skills（业务层）

| Skill | 业务问题 | 依赖 | 状态 |
|---|---|---|---|
| `voc-miner` | 用户抱怨什么、想要什么、为什么流失 | TikTok/X 评论 + App 评论 | ✅ v2.0 |
| `freelance-lead-radar` | 今天该投哪些 Upwork 单、怎么写 proposal | Upwork | ✅ v2.0 |
| `creator-due-diligence` | 该签谁、该投谁、有没有风险 | TikTok/X | 📋 第二批 |
| `competitor-teardown` | 竞品什么内容有效、我们该测什么 | TikTok/X | 📋 第二批 |
| `creator-growth-audit` | 我的账号为什么涨不动 | TikTok/X | 📋 第二批 |
| `aso-pulse` | 评分为什么掉、版本有没有回归 | App Store/Play | 📋 第二批（数据已就绪） |
| `talent-map` | 目标公司在招谁、人才在哪 | LinkedIn | 📋 第二批（公司员工 devOnly） |
| `job-fit-coach` | 这个岗位我配不配、怎么准备 | LinkedIn | 📋 第二批（岗位详情已就绪） |

## 5. 路由表

| 用户说 | 选 |
|---|---|
| 用户抱怨 / 差评 / 产品需求 / 评论分析 / VOC | `voc-miner` |
| 达人 / 网红 / 合作 / 带货 / 背调 | `creator-due-diligence` |
| 竞品 / 对标 / 内容策略 / 爆款 | `competitor-teardown` |
| 招聘 / 人才地图 / 目标公司 / HR | `talent-map` |
| App 评论 / ASO / 评分 / 版本 | `aso-pulse` |
| Upwork / 接单 / 自由职业 / proposal | `freelance-lead-radar` |
| 我的账号 / 涨粉 / 诊断 | `creator-growth-audit` |
| 求职 / 面试 / 岗位匹配 | `job-fit-coach` |
| 不确定 | 问 1–2 个问题，再选 |

## 6. 安装方式

### 自定义 installer（现有用户）

```text
Install the <skill> skill from https://github.com/monsterget-com/skills
```

AI 会把 `skills/<skill>/.` 复制到 `~/.monsterget/skills/<skill>/`。

### npx skills（新用户 / 多 agent）

```bash
npx skills add monsterget-com/skills --skill monsterget-context
npx skills add monsterget-com/skills --skill monsterget-business
npx skills add monsterget-com/skills --skill voc-miner
npx skills add monsterget-com/skills --skill freelance-lead-radar
```

### Plugin（Claude Code / Codex）

```bash
/plugin marketplace add monsterget-com/skills
/plugin install monsterget-skills
```

## 7. 版本

- `scrapers_api: 4`
- extension: `1.8.0+`（TikTok/X/LinkedIn/Upwork）；App Store 评论 `1.12.0+`
- Business skills: `v2.0.0+`

## 8. License

MIT（public repo）。企业私有 Skill 放 private repo。
