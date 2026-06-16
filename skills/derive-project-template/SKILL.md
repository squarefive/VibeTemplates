---
name: derive-project-template
description: Use when deriving project documentation from a project template, initializing AGENTS.md, README.md, or AI collaboration guidance from user-provided context
---

# Derive Project Template

Use this skill to derive a minimal, structured project documentation set from the user's existing context, prompt, or provided project notes.

This skill generates:

- `AGENTS.md`
- `README.md`
- `docs/ai-guidelines/COLLABORATION-PROTOCOL.md`
- `.agents/skills/karpathy-guidelines/SKILL.md`

Core rule:

```text
Extract first. Do not invent. Do not ask by default. Leave missing information explicitly unprovided.
```

## Workflow

1. Extract project information from the current user prompt, conversation context, and provided files.
2. Do not ask follow-up questions by default.
3. If a field cannot be extracted, set it to `_Not provided._`.
4. Convert extracted information into the JSON config fields below.
5. Run `scripts/init_project_docs.py`.
6. Run `scripts/validate_project_docs.py`.
7. Inspect validation output before reporting completion.

When the target project is an Agent development project, also generate an Agent
development context document and validate it with the generated Agent doc
checker.

When initializing a project that will generate or modify code, check whether
the code readability MCP is configured. If it is not configured, tell the user
that this repository provides `tools/code-readability-mcp` and ask before
adding local Codex MCP configuration.

Ask a follow-up question only when the user explicitly requests complete documentation and the missing information blocks generation.

## Output Responsibilities

### `AGENTS.md`

Agent-facing project entry file.

Include only stable project facts and project-specific agent rules:

- guideline index
- project context
- full functional scope and completeness
- module map
- project-specific agent rules

Do not add a current-goal section.

Do include a fixed guideline index that links to
`docs/ai-guidelines/COLLABORATION-PROTOCOL.md` and explains when to read it,
including planning, local file changes, persistent commands, branch changes,
merges, and commits.

When an Agent development context is generated, also include an Agent
development context index linking to the generated `docs/agents/<agent>.md`.

Do not put general AI behavior rules or copy the full user collaboration protocol directly into `AGENTS.md`. General AI coding behavior rules belong in `.agents/skills/karpathy-guidelines/SKILL.md`; collaboration protocol rules belong in `docs/ai-guidelines/COLLABORATION-PROTOCOL.md`.

### `README.md`

Human-facing project entry file.

Include:

- overview
- features
- project structure
- getting started
- development commands

Do not turn `README.md` into an agent rule file.

### `docs/ai-guidelines/COLLABORATION-PROTOCOL.md`

User collaboration protocol.

Copy this file from the bundled template during generation. Do not rewrite it during normal project generation.

This file covers planning requirements, execution confirmation, branch strategy, merge strategy, and commit preferences.

Project-specific rules belong in `AGENTS.md`, not in this file.

### `.agents/skills/karpathy-guidelines/SKILL.md`

General AI coding behavior skill.

Copy this file from the bundled template during generation. Do not rewrite it during normal project generation.

This file provides the `karpathy-guidelines` Codex skill for assumption handling, simplicity, surgical changes, and verification-driven execution.

Project-specific rules belong in `AGENTS.md`, not in this file.

### `docs/agents/<agent_module_name>.md`

Agent development context.

Generate this file only when both `agent_module_name` and
`agent_chinese_name` are extractable. Fill missing Agent document content with
`_Not provided._`; do not invent role boundaries, tools, workflows, data
models, or testing requirements.

Do not generate the raw Agent template into the target project.

### `scripts/check-agent-doc-format.py`

Agent document format checker.

Copy this file only when an Agent development context is generated. The
validator must use it to check the generated Agent document structure.

## Extracted Config Fields

Prepare this JSON shape before generation:

```json
{
  "project_name": "",
  "project_context": "",
  "overview": "",
  "features_section": "",
  "project_structure": "",
  "getting_started": "",
  "development": "",
  "functional_scope_section": "",
  "module_map_section": "",
  "project_specific_agent_rules": "",
  "agent_module_name": "",
  "agent_chinese_name": "",
  "agent_language": "",
  "agent_type": ""
}
```

Use `_Not provided._` for any field that cannot be extracted.

## Field Rules

### `project_name`

Use the repository, product, or template name if available.

If no name is provided, use the target directory name when obvious. Otherwise use `_Not provided._`.

### `project_context`

Extract stable background:

- what the project is
- who it serves
- why it exists
- important constraints

Do not include temporary current work.

### `functional_scope_section`

Describe the full intended feature scope, not only completed work.

Use a table when any feature information is available:

```markdown
| Feature | Status | Notes |
| --- | --- | --- |
| <feature> | <status> | <notes> |
```

Allowed status values:

- `implemented`
- `partial`
- `not-started`
- `deferred`
- `unknown`

Use `unknown` when a feature is extractable but its implementation status is not provided or clearly implied.

Use `_Not provided._` when no feature information is extractable.

### `module_map_section`

List only major modules when the context provides or clearly implies them.

Use a table when any module information is available:

```markdown
| Module | Responsibility | Main Files | Notes |
| --- | --- | --- | --- |
| <module> | <responsibility> | <main files> | <notes> |
```

Use `_Not provided._` when no module information is extractable.

### `project_specific_agent_rules`

Extract only rules specific to the target repository.

Do not repeat general AI coding behavior rules from `.agents/skills/karpathy-guidelines/SKILL.md` or collaboration protocol rules from `docs/ai-guidelines/COLLABORATION-PROTOCOL.md`.

Use `_Not provided._` when no project-specific agent rules are extractable.

### `agent_module_name`

Use the Agent module name when available.

When both `agent_module_name` and `agent_chinese_name` are provided, generate an
Agent development context document at `docs/agents/<agent_module_name>.md`.
Sanitize the filename to allow only letters, numbers, underscores, hyphens, and
dots.

Use `_Not provided._` when no Agent module name is extractable.

### `agent_chinese_name`

Use the Chinese Agent display name when available.

When both `agent_module_name` and `agent_chinese_name` are provided, generate an
Agent development context document whose H1 is:

```markdown
# <agent_chinese_name> Agent 开发上下文
```

Use `_Not provided._` when no Agent Chinese name is extractable.

### `agent_language`

Use the Agent implementation language when available.

Use `_Not provided._` when no language is extractable.

### `agent_type`

Use the Agent type when available, such as `Tool-Using Agent`, `RAG Agent`,
`Workflow Agent`, or `Multi-Agent`.

Use `_Not provided._` when no Agent type is extractable.

## Agent Project Rules

Generate Agent project files only when both `agent_module_name` and
`agent_chinese_name` are provided.

Agent project generation creates:

- `docs/agents/<agent_module_name>.md`
- `scripts/check-agent-doc-format.py`

Agent project generation must not create:

- `docs/templates/agent-development-context.template.md`

Generated Agent documents must not contain unresolved `{{placeholder}}`
values.

## Template Instructions

Templates may contain comments in this format:

```markdown
<!-- TEMPLATE-INSTRUCTION:
Instruction text for the LLM or template maintainer.
-->
```

Generated project files must not contain:

- `TEMPLATE-INSTRUCTION`
- unresolved `{{placeholder}}` values

## Script Usage

Generate project docs:

```powershell
python skills/derive-project-template/scripts/init_project_docs.py --config <config.json> --output <target-project>
```

Validate generated docs:

```powershell
python skills/derive-project-template/scripts/validate_project_docs.py --path <target-project>
```

Validation checks structure, not content completeness. `_Not provided._` is valid output.

General AI coding behavior is validated as a generated Codex skill at `.agents/skills/karpathy-guidelines/SKILL.md`, not as a project-local Markdown guideline under `docs/ai-guidelines/`.

For Agent projects, validation also runs:

```powershell
python scripts/check-agent-doc-format.py docs/agents/<agent>.md
```

## Completion Criteria

Do not report successful initialization unless validation passes.

If validation fails:

1. Read the validation error.
2. Fix the config, template, or generated output source.
3. Regenerate if needed.
4. Rerun validation.
