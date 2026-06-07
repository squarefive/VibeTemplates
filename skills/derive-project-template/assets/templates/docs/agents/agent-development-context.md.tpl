---
module: "{{agent_module_name}}"
title: "{{agent_chinese_name}}"
language: "{{agent_language}}"
agent_type: "{{agent_type}}"
last_updated: "{{last_updated}}"
---

# {{agent_chinese_name}} Agent 开发上下文

> **文档定位**
> 本文档是面向人类开发者和 AI Coding 工具的 Agent 开发上下文文档。
> 它用于约束该 Agent 的角色定位、能力边界、Harness 架构、可调用工具、上下文来源、核心业务流、数据模型和测试要求。
> 本文档不是终端用户说明，也不是运行时 Prompt。

> **AI 阅读契约**
> AI Coding 工具在生成、修改或重构代码时，必须遵守本文档定义的角色边界、工具边界、数据边界和业务流程。
> 不得擅自扩大 Agent 权限，不得绕过声明的 Tool / Service / Repository 直接操作数据库、文件系统、外部接口或其他底层资源。
> 不得新增未声明的核心流程、外部依赖、高风险操作或数据写入行为。
> 涉及具体 Agent 的新增、修改或重构时，AI Coding 工具必须先读取对应 Agent 开发上下文文档，并以该文档作为实现边界和验收依据。
> 如果实现前发现该文档与目标需求不一致，或需要调整 Agent 的角色边界、工具契约、数据模型、核心流程、外部依赖、权限规则等设计内容，必须先修改对应 Agent 文档，并将文档变更提交到本地 Git；在文档版本被锁定后，才能开始修改代码。
> 禁止在同一次提交中混合 Agent 设计文档变更和对应代码实现变更，除非只是修正文档中的错别字、路径或示例。

---

## 1. Agent 定位与能力边界

- **背景**:
  _Not provided._

- **核心价值**:
  _Not provided._

- **Agent 角色**:
  _Not provided._

- **核心目标**:
  1. _Not provided._

- **包含能力**:
  1. _Not provided._

- **不包含能力**:
  1. _Not provided._

- **行为约束**:
  1. _Not provided._

---

## 2. Harness 架构与代码边界

> 本节说明 Agent Harness 的组成，以及各层职责边界。

- **Agent Loop 职责**:
  - _Not provided._

- **Prompt Builder 职责**:
  - _Not provided._

- **Tools 职责**:
  - _Not provided._

- **Services / Repositories 职责**:
  - _Not provided._

- **Storage / External API 职责**:
  - _Not provided._

- **禁止绕过的边界**:
  1. Agent Loop 不得直接操作数据库或文件系统。
  2. LLM 输出不得被视为已持久化事实。
  3. 工具不得绕过权限规则执行高风险操作。
  4. 未在本文档声明的核心依赖不得擅自引入。

- **核心文件 / 目录**:

| 路径 | 职责 |
|---|---|
| _Not provided._ | _Not provided._ |

---

## 3. 可调用工具与工具契约

### 3.1 工具列表

| 工具名 | 工具职责 | 调用时机 | 是否有副作用 | 是否需要确认 |
|---|---|---|---|---|
| _Not provided._ | _Not provided._ | _Not provided._ | _Not provided._ | _Not provided._ |

### 3.2 工具契约

#### _Not provided._

- **职责**:
  _Not provided._

- **输入**:

```json
{
  "not_provided": "_Not provided._"
}
```

- **输出**:

```json
{
  "not_provided": "_Not provided._"
}
```

- **副作用**:
  _Not provided._

- **失败处理**:
  _Not provided._

---

## 4. 上下文来源与记忆边界

- **运行时上下文来源**:
  1. _Not provided._

- **长期记忆来源**:
  1. _Not provided._

- **不得作为长期记忆的内容**:
  1. _Not provided._

- **上下文裁剪规则**:
  1. _Not provided._

---

## 5. 核心业务流

### 5.1 _Not provided._

1. _Not provided._

- **成功条件**:
  _Not provided._

- **失败条件**:
  _Not provided._

- **用户可见反馈**:
  _Not provided._

---

## 6. 数据模型

### 6.1 _Not provided._

| 字段 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| _Not provided._ | _Not provided._ | _Not provided._ | _Not provided._ |

### 6.2 数据约束

1. _Not provided._

---

## 7. 失败模式与降级策略

| 失败模式 | 触发条件 | Agent 行为 | 用户反馈 |
|---|---|---|---|
| _Not provided._ | _Not provided._ | _Not provided._ | _Not provided._ |

- **通用降级原则**:
  1. _Not provided._

---

## 8. 测试要求

- **单元测试**:
  1. _Not provided._

- **集成测试**:
  1. _Not provided._

- **回归测试**:
  1. _Not provided._

- **验收清单**:
  1. _Not provided._

---

## 9. 变更记录

| 日期 | 变更内容 | 变更原因 | 提交 |
|---|---|---|---|
| `{{last_updated}}` | Initial generated agent development context. | Project documentation initialization. | _Not provided._ |
