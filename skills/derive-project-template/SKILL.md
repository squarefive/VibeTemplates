---
name: derive-project-template
description: Use when initializing project documentation or auditing an existing repository for compliance with VibeTemplates docs, AGENTS.md guidance, codebase maps, design principles, and incremental update needs
---

# Derive Project Template

Use this skill to derive a minimal, structured project documentation set from the user's existing context, prompt, or provided project notes.

This skill also audits existing repositories against the VibeTemplates
documentation structure and reports incremental update needs without modifying
files.

## Supported Scenarios

### Initialize Project Documentation

Use when target docs are missing or the user asks to initialize project
documentation.

### Audit Existing Project Documentation

Use when the user asks whether an existing repository conforms to this skill,
partially conforms, or needs updates.

Audit mode must not modify files. Audit mode must report incremental update
suggestions only.

This skill generates:

- `AGENTS.md`
- `README.md`
- `docs/architecture/codebase-map.md`
- `docs/engineering-guidelines/DESIGN-PRINCIPLES.md`
- `docs/ai-guidelines/COLLABORATION-PROTOCOL.md`
- `.agents/skills/karpathy-guidelines/SKILL.md`
- `scripts/check-codebase-map-format.py`

Core rule:

```text
Extract first. Do not invent. Do not ask by default. Leave missing information explicitly unprovided.
```

## Workflow

1. Extract project information from the current user prompt, conversation context, and provided files.
2. Do not ask follow-up questions by default.
3. If a field cannot be extracted, set it to `_Not provided._`.
4. Convert extracted information into the JSON config fields below.
5. Check whether the optional bundled VS Code Markdown translation extension is
   installed, and install the bundled VSIX when the local VS Code CLI is
   available.
6. Run `scripts/init_project_docs.py`.
7. Run `scripts/validate_project_docs.py`.
8. Inspect validation output before reporting completion.

When the target project is an Agent development project, also generate an Agent
development context document and validate it with the generated Agent doc
checker.

When initializing a project that will generate or modify code, check whether
the code readability MCP is configured. If it is not configured, tell the user
that this repository provides `tools/code-readability-mcp` and ask before
adding local Codex MCP configuration.

Ask a follow-up question only when the user explicitly requests complete documentation and the missing information blocks generation.

## Optional VS Code Markdown Translation Extension

This skill bundles an optional local VS Code Markdown translation extension
artifact at:

`assets/tools/vscode/markdown-chinese-preview-translator-0.0.1.vsix`

When running this skill locally, check whether the extension is already
installed. If it is not installed and the bundled VSIX exists, install it with
the local VS Code `code` CLI.

Do not run `npm install`, rebuild the extension, or download extension assets
during this skill.

If the extension is installed or successfully installed, tell the user to
configure the LLM provider in VS Code Settings with these keys:

- `mdTranslate.baseUrl`
- `mdTranslate.apiKey`
- `mdTranslate.model`
- `mdTranslate.targetLanguage`
- `mdTranslate.maxSectionChars`
- `mdTranslate.enableCache`

If the VS Code CLI or bundled VSIX is unavailable, continue the project
documentation initialization and report that the optional extension was not
installed.

## Execution Order

Use this order when initializing project documentation from this skill. The
goal is to produce documentation that reflects only the user's request and
observable target repository facts.

1. Read the current user request, the target repository's existing
   documentation, and the target repository structure before preparing the
   config. Treat the current user request as the highest-priority source when
   sources conflict.
2. Extract project facts into the config fields below. A fact is extractable
   only when it is stated by the user, already present in repository files, or
   directly observable from repository structure.
3. Fill every missing or uncertain field with `_Not provided._`. Do not leave
   empty strings, unresolved placeholders, guessed commands, guessed modules, or
   guessed Agent behavior.
4. Check whether the optional bundled VS Code Markdown translation extension is
   installed. If not installed, install the bundled VSIX only when the local
   `code` CLI is available.
5. Run `scripts/init_project_docs.py` with the prepared config and target output
   path. Do not overwrite existing target files unless the user explicitly asks
   for overwrite behavior.
6. Run `scripts/validate_project_docs.py` against the target output path. If
   validation fails, report the validation errors instead of claiming
   initialization is complete.
7. Report the generated files, skipped files, missing fields, validation result,
   and any explicit assumptions or conflicts found during extraction.

## Extraction Boundaries

Treat information as extractable only when it appears in the user's prompt,
existing repository files, or directly observable project structure.

Do not infer:

- business goals from package names
- development commands from language alone
- module responsibilities from empty directories
- Agent tools, permissions, workflows, memory, or data models unless stated

If information is plausible but not stated, use `_Not provided._`.

## Completion Report

After validation, report using this format:

```markdown
Generated:
- ...

Skipped:
- ...

Missing Fields:
- ...

Validation:
- passed / failed

Notes:
- ...
```

## Audit Order

Audit mode checks whether an existing repository conforms to this skill's
generated documentation structure. It must not modify files.

Use this order:

1. Check whether required documents and scripts exist.
2. For existing files, check whether their content architecture matches the
   current template structure. Check sections, required links, frontmatter,
   unresolved placeholders, and checker results. Do not require exact text
   equality.
3. Report using the fixed audit report format.

Do not run generation scripts or overwrite files during audit mode unless the
user explicitly asks to apply fixes.

Audit recommendations must be incremental. Do not recommend replacing existing
documents when smaller additive changes can bring the repository back into
compliance.

### Fixed Audit Report Format

```markdown
# Project Documentation Audit

Path: <target-path>

Audit Result:
- status: ok | partial | failed

Existing:
- ...

Missing:
- ...

Structure Mismatches:
- ...

Invalid:
- ...

Manual Review:
- ...

Incremental Update Scope:

Add:
- ...

Modify:
- ...

Delete:
- None
```

## Output Responsibilities

### `AGENTS.md`

Agent-facing project entry file.

This file is the AI coding work entry point and top-level documentation index
for a repository. It provides durable project guidance and context loading
rules before AI coding agents start work.

Include only stable project facts and guidance that changes AI development
decisions:

- AGENTS.md role
- context loading rules
- project context
- full functional scope and completeness
- module map
- project-specific agent rules

Do not add a current-goal section.

Do not use `AGENTS.md` as a full documentation dump. Do not record full Agent
design boundaries, code implementation plans, single-task plans, temporary
decisions, or work progress here. Long-form protocols, design rules, code maps,
Agent context, and detailed implementation notes belong in dedicated documents
linked from this file.

Do include fixed context loading rules that explain each linked document's read
conditions, responsibility, and what it does not replace:

- `docs/ai-guidelines/COLLABORATION-PROTOCOL.md`
- `docs/engineering-guidelines/DESIGN-PRINCIPLES.md`
- `docs/architecture/codebase-map.md`
- `docs/agents/<agent>.md` when Agent context is generated

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

### `docs/architecture/codebase-map.md`

AI-facing code navigation document.

Describe the current source directory structure, major modules, and file
responsibilities. This file helps AI coding tools decide where to read, add,
move, or modify source files.

Do not define Agent capability boundaries here. Agent capability boundaries
belong in `docs/agents/<agent_module_name>.md` when an Agent development
context exists.

Do not invent module responsibilities. Fill uncertain responsibilities with
`_Not provided._`.

### `scripts/check-codebase-map-format.py`

Codebase map format checker.

Copy this file during generation. The validator must use it to check
`docs/architecture/codebase-map.md`.

After changing the codebase map, run:

```bash
python3 scripts/check-codebase-map-format.py
```

### `docs/engineering-guidelines/DESIGN-PRINCIPLES.md`

AI-facing software design guidance.

Copy this file from the bundled template during generation. Do not rewrite it
during normal project generation.

This file defines reusable design constraints for module cohesion, dependency
direction, layer boundaries, abstraction restraint, and architecture-level
decisions.

Project-specific architecture facts belong in
`docs/architecture/codebase-map.md` or `AGENTS.md` when they affect AI
development decisions.

### `docs/ai-guidelines/COLLABORATION-PROTOCOL.md`

User collaboration protocol.

Copy this file from the bundled template during generation. Do not rewrite it during normal project generation.

This file covers planning requirements, execution confirmation, branch strategy, merge strategy, and commit preferences.

For documentation changes, this file also requires implementation plans to list
section-level document change details for each affected document.

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

This file records stable Agent design boundaries only. It must not record
single-task plans, temporary implementation steps, Git branch arrangements, work
progress, or current-conversation todos.

When Agent document content is available, fill the Agent template placeholders
from provided context while preserving the template's section, list, table, and
JSON sample structure.

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
  "codebase_map_directory_rows": "",
  "codebase_map_module_sections": "",
  "functional_scope_section": "",
  "module_map_section": "",
  "project_specific_agent_rules": "",
  "agent_module_name": "",
  "agent_chinese_name": "",
  "agent_language": "",
  "agent_type": "",
  "agent_background": "",
  "agent_core_value": "",
  "agent_role": "",
  "agent_core_goals": "",
  "agent_included_capabilities": "",
  "agent_excluded_capabilities": "",
  "agent_behavior_constraints": "",
  "agent_loop_responsibilities": "",
  "agent_prompt_builder_responsibilities": "",
  "agent_tools_responsibilities": "",
  "agent_services_repositories_responsibilities": "",
  "agent_storage_external_api_responsibilities": "",
  "agent_core_files_table_rows": "",
  "agent_tool_table_rows": "",
  "agent_tool_contract_name": "",
  "agent_tool_contract_responsibility": "",
  "agent_tool_input_json_fields": "",
  "agent_tool_output_json_fields": "",
  "agent_tool_side_effects": "",
  "agent_tool_failure_handling": "",
  "agent_runtime_context_sources": "",
  "agent_long_term_memory_sources": "",
  "agent_memory_exclusions": "",
  "agent_context_trimming_rules": "",
  "agent_core_workflow_name": "",
  "agent_core_workflow_steps": "",
  "agent_core_workflow_success_conditions": "",
  "agent_core_workflow_failure_conditions": "",
  "agent_core_workflow_user_feedback": "",
  "agent_data_model_name": "",
  "agent_data_model_table_rows": "",
  "agent_data_constraints": "",
  "agent_failure_mode_table_rows": "",
  "agent_degradation_principles": "",
  "agent_unit_tests": "",
  "agent_integration_tests": "",
  "agent_regression_tests": "",
  "agent_acceptance_checklist": "",
  "agent_initial_commit": ""
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

### `codebase_map_directory_rows`

List current source and documentation directories when the repository structure
is observable.

Use Markdown table rows only:

```markdown
| `src/example/` | _Not provided._ |
```

Use `_Not provided._` for directory responsibilities that are not stated or
directly observable.

### `codebase_map_module_sections`

Describe current modules and file responsibilities when they are stated in
existing repository docs or directly observable from file names and nearby
context.

Use this structure for each module:

```markdown
### <module name>

模块目录：`<module dir>`

模块作用：<module responsibility or _Not provided._>

| 文件 | 作用 |
|---|---|
| `<file path>` | <file responsibility or _Not provided._> |
```

Use a single `_Not provided._` module block when no code structure is
extractable.

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

### Agent document content fields

Use the `agent_*` content fields only for information extractable from the
user prompt, conversation context, or provided files. Do not invent Agent role
boundaries, tools, workflows, data models, memory behavior, failure modes,
permission rules, dependencies, or testing requirements to make the document
look complete.

For list fields, provide Markdown list items without changing the surrounding
template heading. For table row fields, provide Markdown table rows only and
do not repeat the table header. For JSON fields, provide JSON object fields
only and do not include the outer `{}` braces. If a field cannot be extracted,
use `_Not provided._`; the generator supplies structure-specific fallback
content for list, table, and JSON fields.

Content field groups:

- Positioning and boundaries: `agent_background`, `agent_core_value`,
  `agent_role`, `agent_core_goals`, `agent_included_capabilities`,
  `agent_excluded_capabilities`, `agent_behavior_constraints`.
- Harness and code boundaries: `agent_loop_responsibilities`,
  `agent_prompt_builder_responsibilities`, `agent_tools_responsibilities`,
  `agent_services_repositories_responsibilities`,
  `agent_storage_external_api_responsibilities`, `agent_core_files_table_rows`.
- Tools and contracts: `agent_tool_table_rows`, `agent_tool_contract_name`,
  `agent_tool_contract_responsibility`, `agent_tool_input_json_fields`,
  `agent_tool_output_json_fields`, `agent_tool_side_effects`,
  `agent_tool_failure_handling`.
- Context and memory: `agent_runtime_context_sources`,
  `agent_long_term_memory_sources`, `agent_memory_exclusions`,
  `agent_context_trimming_rules`.
- Workflows and data: `agent_core_workflow_name`,
  `agent_core_workflow_steps`, `agent_core_workflow_success_conditions`,
  `agent_core_workflow_failure_conditions`,
  `agent_core_workflow_user_feedback`, `agent_data_model_name`,
  `agent_data_model_table_rows`, `agent_data_constraints`.
- Failure and testing: `agent_failure_mode_table_rows`,
  `agent_degradation_principles`, `agent_unit_tests`,
  `agent_integration_tests`, `agent_regression_tests`,
  `agent_acceptance_checklist`.

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
