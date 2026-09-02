# 六爻起卦 Skill

[![Online](https://img.shields.io/badge/在线体验-6yao.ai-8B5CF6)](https://www.6yao.ai)
[![Agent Skill](https://img.shields.io/badge/Agent-SKILL.md-0F766E)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

可复核的六爻起卦、排盘证据链、解读与连续追问工作流。

> **[在 6yao.ai 直接在线体验](https://www.6yao.ai)** — 无需安装，提供可视化输入、AI 解读、连续追问和报告保存。

## 能力

- 六次三枚铜钱规范化
- 本卦、变卦与动爻
- 证据驱动解读
- 同卦连续追问

核心原则：输入、计算或观察、传统解释、现实行动四层分离。每个重要判断都应能指回盘面字段或可见证据，并明确不确定性。

## 安装

```bash
git clone https://github.com/Leon-Drq/liuyao-skill.git ~/.codex/skills/liuyao-casting
```

也可以把本仓库目录复制到 Claude Code、Codex 或其他支持 `SKILL.md` 的 Agent skills 目录，然后调用 `$liuyao-casting`。

## 使用

从 [SKILL.md](SKILL.md) 开始。它定义触发条件、输入门控、工作流、输出契约和安全边界。`references/` 只在相关步骤按需读取；`scripts/` 中的计算器和客户端应优先于模型手算。

本仓库包含可选的 6yao.ai API 客户端；认证信息只从环境变量读取。

## 在线版本

- 当前 Skill：[立即体验](https://www.6yao.ai)
- 6yao.ai 工具总览：[www.6yao.ai/tools](https://www.6yao.ai/tools)
- 作者的更多开源项目：[github.com/Leon-Drq](https://github.com/Leon-Drq)

## 隐私与边界

精确出生时间、地点、照片和关系记录属于敏感个人资料，不应提交到 GitHub issue 或版本库。传统术数与 AI 解读用于文化学习、娱乐、自我观察和现实复盘，不构成医疗、法律、投资、财务或人身安全建议。

## License

MIT。第三方依赖和资料仍遵循各自许可证或公有领域规则。
