# TikTok Collector — Value-First Onboarding

> Read this before the first user-facing message after installation, and whenever
> the user asks "怎么用 / how to use / 你能做什么".
>
> **The first message must sell outcomes, not setup.** The user should choose a
> business goal before seeing any installation step.

## The one rule

**Value first, setup second.**

- The first message contains **0 installation steps**.
- Show 4 TikTok business outcomes and let the user choose.
- Only after the choice do you show the mini plan, ask for one input, and show
  the setup that this specific task needs.

This document is the single source of truth for the flow. `AGENTS.md` and
`SKILL.md` reference it; keep their first-message copy in sync.

---

## State machine

```text
install
  -> value_menu
  -> mini_plan
  -> one_input
  -> just_in_time_setup
  -> first_sample
  -> deliver
  -> deepen | switch_goal | done
```

Persist the stage in `~/.monsterget/state.json` with `set-onboarding.sh`:

```bash
bash "$SCRIPTS/set-onboarding.sh" stage value_menu
bash "$SCRIPTS/set-onboarding.sh" goal growth sub competitor input "mike tyson" stage first_sample
```

Keys:

| Key | Values | Meaning |
|---|---|---|
| `tiktok_onboarding_goal` | `growth` / `creator` / `voc` / `trend` | The business outcome the user picked |
| `tiktok_onboarding_sub` | `competitor` / `creator` / `comments` / `tag` | The concrete task inside that outcome |
| `tiktok_onboarding_input` | free text | Keyword, hashtag, handle, or video URL |
| `tiktok_onboarding_stage` | `value_menu` / `mini_plan` / `one_input` / `setup` / `first_sample` / `delivered` / `done` | Where the user is |

The `tiktok_` prefix keeps these keys separate from other collectors that share
the same `~/.monsterget/state.json`.

### When to set the stage

| Moment | Command |
|---|---|
| Before showing the value menu | `set-onboarding.sh stage value_menu` |
| After the user picks a goal / shows the mini plan | `set-onboarding.sh goal growth sub competitor stage mini_plan` |
| After asking for the one input | `set-onboarding.sh stage one_input` |
| After the user gives the input / before setup | `set-onboarding.sh input "mike tyson" stage setup` |
| Before the first scrape | `set-onboarding.sh stage first_sample` |
| After delivering the result | `set-onboarding.sh stage delivered` |
| When the user says they are done | `set-onboarding.sh stage done` |

The goal/sub mapping is in the menu table below. Use the actual value the user
chose; these are examples.

---

## Step 0 — Returning user

Read `~/.monsterget/state.json` before greeting.

If `tiktok_onboarding_goal` exists and `tiktok_onboarding_stage` is an active stage
(`mini_plan`, `one_input`, `setup`, `first_sample`, `delivered`), greet with:

```text
上次你在做「{goal_label}」，要继续吗？

A. 继续上次的关键词/账号
B. 换一个关键词/账号
C. 换一个目标
```

- A -> go to the mini plan with the saved `tiktok_onboarding_input`.
- B -> ask for the new input, then go to the mini plan.
- C -> show the value menu.
- If `tiktok_onboarding_stage` is `done`, `value_menu`, or missing -> show the value menu.

Do not show the value menu again unless the user picks C.

---

## Step 1 — Value menu (the first message)

Show exactly 4 options plus the "不确定" escape hatch. Keep the message short
and scannable. Do not add setup steps, examples of CSV columns, or implementation
details.

### Menu mapping

| # | Label | `goal` | `sub` | What the user gets |
|---|---|---|---|---|
| 1 | 找爆款/竞品打法 | `growth` | `competitor` | Top videos + engagement rate + 3 replicable content angles |
| 2 | 找达人/创作者 | `creator` | `creator` | Creator list + followers/engagement + profile links |
| 3 | 听用户声音 | `voc` | `comments` | Comment themes + verbatim quotes + product opportunities |
| 4 | 追标签/趋势 | `trend` | `tag` | Hashtag video list + recent winners + trend notes |

### Exact zh-CN copy

```text
装好了 ✅ 先不用配置。
你想先用 TikTok 数据达成什么？回复数字：

1️⃣ 找爆款/竞品打法
   抓关键词或竞品账号下的热门视频，按互动率找选题

2️⃣ 找达人/创作者
   按内容方向找创作者，看粉丝和互动

3️⃣ 听用户声音
   抓视频评论，找真实需求/不满

4️⃣ 追标签/趋势
   看某个标签最近什么内容在涨

回复 1–4；不确定就回复"你推荐"。
```

For other languages, translate the same structure. Do not add setup steps.

---

## Step 2 — Mini plan (after the user chooses)

Show four things:

1. What they will get (deliverable).
2. The first sample size and that it is a **Quick sample**, not a full report.
3. What one input you need.
4. The estimated time.

### Example — choice 1, 找爆款/竞品打法

```text
好，选「找爆款/竞品打法」。

先跑一个 3–5 分钟的小样（Quick 档，明确标注是小样）：
- 50 条相关视频：标题/播放/点赞/评论/发布时间
- 按互动率排序，给你 Top 10
- 3 个可复制的选题方向

只需要 1 个信息：关键词或竞品账号。
没有的话回复"你推荐"，我先用行业默认词。
```

### Example — choice 2, 找达人/创作者

```text
好，选「找达人/创作者」。

先跑一个 3–5 分钟的小样（Quick 档）：
- 30 个相关创作者：粉丝、互动、简介、主页链接
- 按粉丝量 + 互动率排序
- 标出 3 个最值得进一步看的账号

只需要 1 个信息：内容方向/关键词，或者你已知的账号。
没有的话回复"你推荐"。
```

### Example — choice 3, 听用户声音

```text
好，选「听用户声音」。

先跑一个 5–8 分钟的小样（Quick 档）：
- 如果给视频链接：抓 50 条评论
- 如果给关键词：先找 1–3 条高互动视频，再抓 50 条评论/条
- 提炼 3–5 个主题 + 用户原话

只需要 1 个信息：视频链接或关键词。
没有的话回复"你推荐"。
```

### Example — choice 4, 追标签/趋势

```text
好，选「追标签/趋势」。

先跑一个 3–5 分钟的小样（Quick 档）：
- 30 条标签下的视频：播放、点赞、评论、发布时间
- 找出最近互动最高的内容
- 给你 3 条趋势观察

只需要 1 个信息：标签名（不用带 #）。
没有的话回复"你推荐"。
```

### Task mapping

| Choice | `pagePath` | `param` | Quick sample | Notes |
|---|---|---|---|---|
| 1 找爆款 | `/tiktok-search-video` (keyword) or `/tiktok-user-videos` (competitor) | `query` / `username` | 50 | Sort by engagement rate in the summary |
| 2 找达人 | `/tiktok-search-user` | `query` | 30 | Sort by followers + engagement |
| 3 听用户声音 | `/tiktok-comments` | `value` (video URL) | 50 | If keyword: search 10 videos first, then comments on 1–3 |
| 4 追标签 | `/tiktok-tag` | `query` | 30 | No `#` in the value |

Full data plans and Standard/Deep tiers are in `SKILL.md` and
`../../DATA-STANDARDS.md`. The first sample is deliberately Quick and must be
labelled as such.

### How to produce the first insights

| Choice | Compute | Show |
|---|---|---|
| 1 找爆款 | Engagement rate = (likes + comments) / views; sort descending | Top 10 table + 3 content angles (hook/topic/format) |
| 2 找达人 | Followers + average engagement; flag outliers | Top 10 creators + 3 to vet further + risk notes |
| 3 听用户声音 | Group comments into 3–5 themes; count mentions; pick 1–2 quotes per theme | Themes + verbatim quotes + 3 product opportunities |
| 4 追标签 | Sort by views/likes/comments and recency | Top 10 videos + 3 trend observations |

Keep the analysis lightweight for the Quick sample and say it is directional.
Never fabricate a metric: if a CSV field is missing, say so.

---

## Step 3 — Ask exactly one input

Ask only for the input that the chosen task needs. Always offer a default:

- 1 找爆款: keyword or competitor account.
- 2 找达人: content direction/keyword, or known handles.
- 3 听用户声音: video URL or keyword.
- 4 追标签: hashtag name.

If the user says "你推荐" or "不知道", pick a sensible default from their
previous context or a broad category term, say what you picked, and continue.
Do not ask a second question before running the sample.

---

## Step 4 — Just-in-time setup

Only now show the setup. Read `state.json` first:

- If `browser_pref` is already set, skip the installation guide and go to the
  pre-task reminder in `SKILL.md` Step 1.
- If `browser_pref` is missing, show the 3 things below.

### First-time setup copy (zh-CN)

```text
收到。要拿到完整数据，需要先准备 3 件事（约 3 分钟，只需一次）：
① 安装 MonsterGet 扩展 → https://monsterget.com/install
② 登录 monsterget.com → https://monsterget.com
③ 登录 TikTok → https://www.tiktok.com

装好扩展后告诉我装在了哪个浏览器（回复"Edge"或"Chrome"），全部准备好了回复"好了"。
```

Then:

```bash
bash "$SCRIPTS/choose-browser.sh" edge   # or chrome
```

Rules:

- **Never run any detection script, never scan the disk, never verify
  programmatically.** The user's manual confirmation is the only check.
- All three things must be in the **same browser**.
- If the user later switches browsers, repeat this setup.
- Do not show the setup before the value menu and the one input.

---

## Step 5 — First sample + deliver

Before the scrape, follow `SKILL.md` Step 1 (pre-task reminder) and say the
account-risk line once per batch:

```text
这次抓取会使用你自己的 TikTok 账号；批量采集可能违反 TikTok 的服务条款，账号和合规责任由你承担。
```

Then run the Quick sample with `run-scrape.sh` using the counts in the task
mapping table. Tell the user:

```text
✅ 准备好了，开始抓取。预计 3–5 分钟，抓完我直接把 CSV 和摘要发你。
```

After the CSV is ready, deliver in this shape:

```text
结果好了 ✅
- {rowCount} 条，Top 3：{...}
- CSV：{path}
- 3 条可执行洞察：{...}

下一步：
A. 扩到 {Standard count} 条，做完整分析（Standard）
B. 换一个关键词/账号对比
C. 换一个目标
```

Rules:

- Show the CSV path and 3–5 preview rows, not the whole file.
- The first sample is directional. Say "小样/Quick" and offer the Standard tier.
- Do not call a Quick sample a "完整报告".
- If the result is empty, use the failure checklist in `SKILL.md`; do not
  silently retry with a different query.

---

## Step 6 — Persist and close the loop

After the first result:

```bash
bash "$SCRIPTS/set-onboarding.sh" goal growth sub competitor input "mike tyson" stage delivered
```

- If the user chooses A (deepen) -> run the Standard plan, keep the same goal.
- If the user chooses B (switch input) -> update `tiktok_onboarding_input`, keep the goal.
- If the user chooses C (switch goal) -> set stage `value_menu`, show the menu.
- If the user says they are done -> set stage `done`.

On the next session, use Step 0 to offer "继续上次的吗？".

---

## Branches

### "不确定" / "你推荐"

Ask at most 2 questions:

1. 你是做什么的/卖什么？
2. 你现在最想解决的是：没流量、没客户、产品不知道改什么、还是找达人/招人？

Then recommend 1–2 options with a one-line reason and ask the user to pick.
Do not dump all 4 options again.

### User gives a direct task before choosing

Example: "抓取 mike tyson 50 条".

- Acknowledge the outcome in one line: "好，做「找爆款/竞品打法」，先跑 50 条小样。"
- Skip the menu.
- Go to Step 3 (one input is already provided) and then Step 4 (setup if needed).
- Persist `goal=growth`, `sub=competitor`.

### The user asks for another platform

If the user asks for LinkedIn, X, Upwork, or App Store data:

```text
这个目标需要 {platform} collector，当前装的是 TikTok collector。
你可以先装 {skill}，或者我用 TikTok 数据做一个近似版本。
```

Do not pretend to have data from a platform that is not installed.

### The user asks "怎么用"

Show the 4-option value menu (or 2–3 examples) and ask them to pick. Do not show
this document, bash commands, script paths, API endpoints, taskIds, or state
files.

### The user is an advanced user who only wants raw data

Route directly to the collector with a one-line value framing, then ask for the
keyword/URL. Skip the business analysis layer, but still do the JIT setup.

---

## Guardrails

- Never show bash, script paths, API endpoints, taskIds, polling logic,
  `state.json`, or `VERSION.json` to the user.
- Never show the 3 setup steps before the value menu.
- Never ask more than one input at a time.
- Always offer "你推荐 / 用默认".
- Always label the first sample as "小样/Quick"; never call it a full report.
- Never promise private data, demographics, transcripts, or ad libraries.
- Keep the one-browser rule.
- Keep the existing pre-task reminder and account-risk line.

---

## Acceptance checklist

- [ ] First message has 4 outcomes and 0 setup steps.
- [ ] The user can choose with a single number.
- [ ] The mini plan states deliverable, one input, time, and sample size.
- [ ] Setup appears only after the user chooses and gives the input.
- [ ] The first result arrives in the same conversation.
- [ ] The next-step menu offers deepen / switch / done.
- [ ] A returning user is recognized and offered "继续上次的吗？".
- [ ] No implementation details appear in user-facing text.
