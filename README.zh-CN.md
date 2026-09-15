# 🛡️ MonsterGet Skills — 为 AI 打造的反封禁网页采集

> **告别封号。通过你自己的真实浏览器采集 TikTok —— 用你已登录的会话。AI 全自动，零配置，永久免费。**

[English](README.md) · **简体中文** · [日本語](README.ja.md) · [Español](README.es.md) · [Português](README.pt.md)

[![永久免费](https://img.shields.io/badge/🆓-永久免费-22bb33?style=flat-square)](https://monsterget.com)
[![AI 原生](https://img.shields.io/badge/🤖-AI%20原生-2196F3?style=flat-square)](https://monsterget.com)
[![1000万条](https://img.shields.io/badge/📦-注册即享%201000万条-FF9800?style=flat-square)](https://monsterget.com)

---

## ✨ 这是什么？

**MonsterGet Skills** 让任何 AI 助手变身 TikTok 数据引擎 —— 而且不会让你的账号被封。

网页采集有一个公开的秘密：**服务端采集器会被封。** TikTok、Instagram、LinkedIn —— 它们都在对抗无头浏览器、机房 IP 和代理池。你加固，它们封得更狠。这是一场你注定输的军备竞赛。

MonsterGet 换了个玩法：**采集发生在你自己的浏览器里**，用你真实的登录会话。TikTok 看到的是一个真实用户。你拿到的是数据。

| 方案 | 反封禁 | 配置成本 | 费用 |
|------|--------|---------|------|
| ❌ 服务端采集器 | ❌ 被封 | 数小时配置 | 代理 + 服务器 |
| ❌ 无头浏览器 | ❌ 很快被识别 | Selenium/Playwright | 服务器账单 |
| ✅ **MonsterGet（你的浏览器）** | ✅ **隐形** | **2 分钟，一次性** | **🆓 免费额度：1000万条** |

## 🚀 能做什么？

| 使用场景 | 拿到的数据 |
|---------|-----------|
| 🔍 **达人挖掘** | 按关键词搜索创作者 → CSV 含简介、粉丝数、头像 |
| 🎬 **视频调研** | 按关键词搜索视频 → CSV 含播放、点赞、评论、分享链接 |
| 🏷️ **标签情报** | 输入一个标签 → 该标签下所有视频的 CSV |
| 👤 **账号审核** | 获取某创作者发布的全部视频 → 完整数据 |
| 📊 **批量拉取主页** | 一次 50+ 个账号 → 一个 CSV，聚合统计 |

所有结果都是干净的 CSV 文件 —— Excel 打开、导入分析工具，或喂回给你的 AI。

## 🤖 AI 原生设计

兼容**所有**主流 AI 编程工具：

`Claude Code` · `Codex CLI` · `Cursor` · `Windsurf` · `Cline` · `Roo Code` · `Kilo Code` · `Copilot` · `Gemini CLI` · `Zed` · `Aider` · `Continue` · `Junie` · `Warp` · `Devin`

该 skill **与具体 agent 无关**：所有 shell 操作都由协议化的独立脚本完成，输出 JSON，无论底层驱动 agent 是 Claude Code 还是其他工具，行为完全一致。

AI 负责全部编排：

```
🧠 AI："我需要 TikTok 数据做市场调研"
   ↓
🔗 在你的浏览器中打开一个 URL
   ↓
🌐 你真实的 TikTok 会话 + MonsterGet 扩展完成采集
   ↓
📥 AI 下载 CSV 并交付给你
```

**你永远不用碰 Python、Selenium、代理或验证码。** AI 做编排，你的浏览器做采集。

## 🎁 定价，讲道理的那种

| 档位 | 额度 | 并发窗口 | 价格 |
|------|------|---------|------|
| 免费 | **1000万条** | 1 | **🆓 $0 —— 永久** |
| 会员 | 更多 | 更多并行 | 合理 |

没有套路。没有"14 天后过期"的假免费。1000 万条是真的。

## 💬 用户怎么说

> *"我当时在轮换 50 个代理，TikTok 还是封我。MonsterGet 直接就能跑 —— 每次都是第一次就成了。"*
> —— **电商数据分析师**

> *"我跟我的 Claude 说'帮我找 200 个美妆领域的 TikTok 达人'。3 分钟后回来一个 CSV。一行代码都没写。"*
> —— **营销机构主理人**

> *"配置花了 2 分钟。我已经采集了 200 万条。还在免费用量内。这感觉不太合法，但显然没问题。"*
> —— **增长黑客**

## ⏱️ 首次配置 —— 2 分钟，一次性

| 步骤 | 做什么 |
|------|--------|
| 1 | [注册免费账号](https://monsterget.com) —— 邮箱 + 密码，完成 |
| 2 | [安装浏览器扩展](https://monsterget.com/install) —— Chrome/Edge，一键 |
| 3 | 把 skill 文件夹复制到你的 AI 客户端 → 完成 |

之后，**每次采集都是瞬间完成。** 再也不用配置。永远。

## 📦 可用的 Skill

| Skill | 功能 | 平台 |
|-------|------|------|
| [🎵 tiktok-collector](tiktok-collector/SKILL.md) | TikTok 视频搜索、达人挖掘、标签采集、达人资料导出为 CSV | TikTok |

*更多平台即将支持（LinkedIn、Instagram、X/Twitter、YouTube…）。开 issue 投票。*

## 🔧 安装方法

**不用记任何命令。** 打开你的 AI 助手（Claude Code / Codex / Cursor / Cline…），在对话框里发：

> 💬 安装 skill tiktok-collector，https://github.com/rosstzc/monsterget.com-skills

AI 会自动克隆仓库，安装运行时，并配置自身。

### AI 具体做的事

1. 克隆本仓库
2. 复制 `tiktok-collector/` → `~/.monsterget/skill/` —— **共享运行时目录**
3. 在自己对应的 rules 文件中添加一行指针

因为运行时放在一个固定位置（`~/.monsterget/skill/`），**你所有 AI 客户端共享它**。安装一次，Claude Code、Codex、Cursor、Cline 都能用。

**想手动安装？** 见 [tiktok-collector/INSTALL.md](tiktok-collector/INSTALL.md) —— 有手动步骤和每个客户端的指针位置。

**没有 shell 权限**（比如纯网页版 ChatGPT）？把 [`tiktok-collector/SKILL.md`](tiktok-collector/SKILL.md) 的内容粘贴到你的自定义指令中，AI 会文字指引你完成每一步。

## 🧠 架构（实际发生了什么）

```
AI ──▶ 生成 taskId + 打开浏览器 URL
         │
你的浏览器 ──▶ MonsterGet 扩展在你的 TikTok 标签页中执行采集
                   │
                数据行流入服务器缓冲区 ──▶ AI 轮询并下载 CSV
```

**交付后服务器不留任何数据。** 隐私优先设计。

## 📄 许可证

MIT —— 见 [LICENSE](LICENSE)。

---

> **准备好不再跟反爬系统对抗了吗？** [免费注册 →](https://monsterget.com)
>
> *1000 万条额度。一个浏览器会话。零账号被封。*
