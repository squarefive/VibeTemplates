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
<!-- TEMPLATE-INSTRUCTION:
Extract the Agent background, value, role, goals, capabilities, exclusions, and behavior constraints from provided context.
If a field cannot be extracted, render its configured missing-value fallback.
Do not invent role boundaries, capabilities, or behavior constraints.
-->

- **背景**:
  {{agent_background}}

- **核心价值**:
  {{agent_core_value}}

- **Agent 角色**:
  {{agent_role}}

- **核心目标**:
  {{agent_core_goals}}

- **包含能力**:
  {{agent_included_capabilities}}

- **不包含能力**:
  {{agent_excluded_capabilities}}

- **行为约束**:
  {{agent_behavior_constraints}}

---

## 2. Harness 架构与代码边界
<!-- TEMPLATE-INSTRUCTION:
Extract the Agent Harness layers, responsibility boundaries, and core files from provided context.
Keep fixed forbidden-boundary rules unless project-specific context explicitly tightens them.
Do not invent implementation files, repositories, services, or external dependencies.
-->

> 本节说明 Agent Harness 的组成，以及各层职责边界。

- **Agent Loop 职责**:
  {{agent_loop_responsibilities}}

- **Prompt Builder 职责**:
  {{agent_prompt_builder_responsibilities}}

- **Tools 职责**:
  {{agent_tools_responsibilities}}

- **Services / Repositories 职责**:
  {{agent_services_repositories_responsibilities}}

- **Storage / External API 职责**:
  {{agent_storage_external_api_responsibilities}}

- **禁止绕过的边界**:
  1. Agent Loop 不得直接操作数据库或文件系统。
  2. LLM 输出不得被视为已持久化事实。
  3. 工具不得绕过权限规则执行高风险操作。
  4. 未在本文档声明的核心依赖不得擅自引入。

- **核心文件 / 目录**:

| 路径 | 职责 |
|---|---|
{{agent_core_files_table_rows}}

---

## 3. 可调用工具与工具契约
<!-- TEMPLATE-INSTRUCTION:
Extract declared callable tools and tool contracts from provided context.
Table row fields must include Markdown table rows only. JSON field placeholders must include JSON object fields only, without outer braces.
Do not invent tools, side effects, confirmation rules, inputs, or outputs.
-->

### 3.1 工具列表

| 工具名 | 工具职责 | 调用时机 | 是否有副作用 | 是否需要确认 |
|---|---|---|---|---|
{{agent_tool_table_rows}}

### 3.2 工具契约

#### {{agent_tool_contract_name}}

- **职责**:
  {{agent_tool_contract_responsibility}}

- **输入**:

```json
{
  {{agent_tool_input_json_fields}}
}
```

- **输出**:

```json
{
  {{agent_tool_output_json_fields}}
}
```

- **副作用**:
  {{agent_tool_side_effects}}

- **失败处理**:
  {{agent_tool_failure_handling}}

---

## 4. 上下文来源与记忆边界
<!-- TEMPLATE-INSTRUCTION:
Extract runtime context sources, long-term memory sources, memory exclusions, and context trimming rules from provided context.
Do not invent memory behavior or persistence sources.
-->

- **运行时上下文来源**:
  {{agent_runtime_context_sources}}

- **长期记忆来源**:
  {{agent_long_term_memory_sources}}

- **不得作为长期记忆的内容**:
  {{agent_memory_exclusions}}

- **上下文裁剪规则**:
  {{agent_context_trimming_rules}}

---

## 5. 核心业务流
<!-- TEMPLATE-INSTRUCTION:
Extract core workflows, success conditions, failure conditions, and user-visible feedback from provided context.
Do not invent workflows or product behavior.
-->

### 5.1 {{agent_core_workflow_name}}

{{agent_core_workflow_steps}}

- **成功条件**:
  {{agent_core_workflow_success_conditions}}

- **失败条件**:
  {{agent_core_workflow_failure_conditions}}

- **用户可见反馈**:
  {{agent_core_workflow_user_feedback}}

---

## 6. 数据模型
<!-- TEMPLATE-INSTRUCTION:
Extract declared data models and constraints from provided context.
Table row fields must include Markdown table rows only. Do not invent schemas or persistence requirements.
-->

### 6.1 {{agent_data_model_name}}

| 字段 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
{{agent_data_model_table_rows}}

### 6.2 数据约束

{{agent_data_constraints}}

---

## 7. 失败模式与降级策略
<!-- TEMPLATE-INSTRUCTION:
Extract failure modes and degradation principles from provided context.
Table row fields must include Markdown table rows only. Do not invent operational failure behavior.
-->

| 失败模式 | 触发条件 | Agent 行为 | 用户反馈 |
|---|---|---|---|
{{agent_failure_mode_table_rows}}

- **通用降级原则**:
  {{agent_degradation_principles}}

---

## 8. 测试要求
<!-- TEMPLATE-INSTRUCTION:
Extract unit, integration, regression, and acceptance testing requirements from provided context.
Do not invent test coverage promises or unsupported verification requirements.
-->

- **单元测试**:
  {{agent_unit_tests}}

- **集成测试**:
  {{agent_integration_tests}}

- **回归测试**:
  {{agent_regression_tests}}

- **验收清单**:
  {{agent_acceptance_checklist}}

---

## 9. 变更记录

| 日期 | 变更内容 | 变更原因 | 提交 |
|---|---|---|---|
| `{{last_updated}}` | Initial generated agent development context. | Project documentation initialization. | {{agent_initial_commit}} |
