---
name: derive-project-template
description: Use when deriving project documentation from a project template, initializing AGENTS.md, README.md, or AI collaboration guidance from user-provided context
---

# Derive Project Template

Use this skill to derive a minimal, structured project documentation set from the user's existing context, prompt, or provided project notes.

This skill generates:

- `AGENTS.md`
- `README.md`
- `docs/ai-guidelines/AI-COLLABORATION.md`

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

Ask a follow-up question only when the user explicitly requests complete documentation and the missing information blocks generation.

## Output Responsibilities

### `AGENTS.md`

Agent-facing project entry file.

Include only stable project facts and project-specific agent rules:

- project context
- full functional scope and completeness
- module map
- project-specific agent rules

Do not add a current-goal section.

Do not put general AI behavior rules in `AGENTS.md`. General AI behavior rules belong in `docs/ai-guidelines/AI-COLLABORATION.md`.

### `README.md`

Human-facing project entry file.

Include:

- overview
- features
- project structure
- getting started
- development commands

Do not turn `README.md` into an agent rule file.

### `docs/ai-guidelines/AI-COLLABORATION.md`

General AI collaboration guidance.

Copy this file from the bundled template during generation. Do not rewrite it during normal project generation.

Project-specific rules belong in `AGENTS.md`, not in this file.

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
  "project_specific_agent_rules": ""
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

Do not repeat general rules from `AI-COLLABORATION.md`.

Use `_Not provided._` when no project-specific agent rules are extractable.

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

## Completion Criteria

Do not report successful initialization unless validation passes.

If validation fails:

1. Read the validation error.
2. Fix the config, template, or generated output source.
3. Regenerate if needed.
4. Rerun validation.
