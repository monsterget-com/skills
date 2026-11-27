# 5 分钟上手

> 目标：装好、说出第一句话、拿到第一份结果。
> 不需要懂代码，不需要 API key。

---

## 0. 你需要准备什么

| 东西 | 说明 |
|---|---|
| 一个支持本地 skill 的 AI 客户端 | Claude Code、Codex、Cursor、Cline、Windsurf、WorkBuddy、Kimi 等桌面端 / IDE；浏览器网页版通常装不了 skill |
| Chrome 或 Edge | 采集发生在你自己的浏览器里 |
| MonsterGet 账号 | 免费注册：https://monsterget.com |
| MonsterGet 扩展 | 安装页：https://monsterget.com/install |
| 目标平台账号 | TikTok / X / LinkedIn / Upwork 需要你已登录；App Store / Google Play 评论不需要商店登录 |

> 一条铁律：**扩展、monsterget.com 登录、目标平台登录，必须在同一个浏览器里。**

---

## 1. 安装 skill

### 方案 A：只装你要的（最小）

在 AI 对话框里发：

> 安装 skill tiktok-collector，https://github.com/monsterget-com/skills

把 `tiktok-collector` 换成你要的平台：

| 你要做什么 | 装这个 |
|---|---|
| TikTok 视频 / 达人 / 评论 | `tiktok-collector` |
| X 搜索 / 推文 / 评论 | `x-collector` |
| LinkedIn 档案 / 岗位 / 人才 | `linkedin-collector` |
| Upwork 岗位 | `upwork-collector` |
| App Store / Google Play 评论 | `app-reviews-collector` |
| 把 App 评论做成 HTML 报告 | 再装 `app-reviews-analyst` |

### 方案 B：全套（推荐给要长期做分析的人）

一次发给 AI：

> 请从 https://github.com/monsterget-com/skills 安装这些 skill：
> tiktok-collector、x-collector、linkedin-collector、upwork-collector、
> app-reviews-collector、app-reviews-analyst、monsterget-context、
> monsterget-business、voc-miner、freelance-lead-radar

如果 AI 只装了其中一个，把剩下的分开再发一次即可。

> 安装位置：`~/.monsterget/skills/<skill>/`。升级时重新发一次安装指令即可。

---

## 2. 第一次设置（约 3 分钟，只需一次）

装好后，AI 会引导你完成 3 件事：

1. 安装扩展：https://monsterget.com/install
2. 登录 monsterget.com：https://monsterget.com
3. 登录目标平台（例如 tiktok.com）

都在**同一个浏览器**里完成，然后告诉 AI「好了」。
App Store / Google Play 评论不需要登录商店。

> AI 不会扫描你的磁盘、不会开测试窗口；它只按你说的浏览器执行。

---

## 3. 说出第一句话

不用学命令。直接说你要的**决策**和**对象**。

### App 评论（已有完整报告能力）

> 分析一下 CapCut 在 App Store 和 Google Play 最近 90 天的 1–2 星评论，
> 给我一份 HTML 报告，重点看 iOS 和 Android 骂得有什么不同。

你会得到：`report.html` + `metrics.json` + `tables/*.csv`。

### TikTok 内容 / 达人（采集已就绪）

> 我想看 @theordinary 最近 100 条视频的内容打法，
> 给我 CSV，并按互动率排出 Top 10，告诉我 3 个可复制的选题方向。

### Upwork 接单（已有业务 skill）

> 我是 React 前端，$60/小时，只做远程，
> 帮我筛最近 14 天的 Upwork 单，给我 Top 10 和 proposal 草稿。

### LinkedIn 岗位 / 人才（采集已就绪）

> 帮我扫一下深圳「跨境电商运营」岗位最近一个月的变化，
> 按公司、薪资、技能要求整理成表。

> 更多说法见 [业务菜单](business-menu.md)。

---

## 4. 你会拿到什么

| 文件 | 用途 |
|---|---|
| `*.csv` | 原始采集数据，可以用 Excel / Numbers 打开 |
| `manifest.json` | 这次抓了什么、多少条、什么时候抓的 |
| `metrics.json` | 所有指标数字；报告里的数字都来自这里 |
| `report.html` | 单文件报告，浏览器打开，可直接打印成 PDF |
| `tables/*.csv` | 评分分布、主题占比、每日趋势、原话等表格 |

报告里的每个数字都能回溯到 CSV 或 `metrics.json`。
如果某个字段缺失，报告会写"暂无"或"不参与计算"，不会编。

---

## 5. Quick / Standard / Deep 怎么选

第一次默认给你 **Quick 小样**：3–5 分钟，只用来判断方向。
要写进报告、做决策，升到 **Standard**。

| 档位 | 适合 | 典型量级 | 时间 |
|---|---|---|---|
| Quick | 先看看有没有信号 | 50–200 条/来源 | 3–5 分钟 |
| Standard | 正常业务报告 | 500–2,000 条/来源 | 8–20 分钟 |
| Deep | 竞品 / 多市场 / 高 stakes | 2,000–4,000 条 | 30–60 分钟 |

> Quick 不是"完整报告"，结论只能说"方向性"。完整对照见 [FAQ](faq.md)。

---

## 6. 拿到结果之后

你可以直接说：

- 「只看最近 30 天」→ 通常不用重抓
- 「加一个竞品」→ 需要补抓，AI 会先报次数
- 「按版本拆开看」→ 取决于数据里有没有版本字段
- 「给我 20 个达人名单」→ 从表里导出，不用重抓
- 「做成小红书卡片 / 视频脚本」→ 交给内容交付能力（规划中）

每次补抓前，AI 应该先告诉你：**抓什么、多少条、大概多久、缺什么**。

---

## 7. 出问题了

| 现象 | 先检查 |
|---|---|
| 浏览器没反应 / 没打开 | 扩展装了吗？装在你告诉 AI 的那个浏览器里吗？ |
| 一直排队 / `not_found` | monsterget.com 登录了吗？目标平台登录了吗？窗口被遮挡了吗？ |
| 抓到 0 条 | 链接/关键词对吗？换一个更宽的关键词；平台可能没有公开数据 |
| 报告没生成 | 有 Python 3.10+ 吗？CSV 列名对吗？样本是否低于最小门槛？ |
| 只有部分数据 | 报告会写缺失；不要把它当成全量结论 |

完整排查见 [FAQ](faq.md)。
