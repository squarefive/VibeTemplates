# AGENTS.md

## Guideline Index

For planning, local file changes, persistent commands, branch changes, merges,
and commits, read and follow:

- `docs/ai-guidelines/COLLABORATION-PROTOCOL.md`

When the user says "按照规约", "按规约", "给出计划", "先给计划",
or asks for a plan before execution, read that file completely before responding.

{{agent_development_context_index}}
## Project Context
<!-- TEMPLATE-INSTRUCTION:
Extract stable project background from the user's context.
Include what the project is, who it serves, why it exists, and important constraints.
If not provided, render: _Not provided._
Do not include temporary current goals.
-->
{{project_context}}

## Functional Scope And Completeness
<!-- TEMPLATE-INSTRUCTION:
Extract the full intended feature scope from the user's context.
Include implementation status only when it is provided or clearly implied.
If status is unclear, use unknown.
If no feature information is provided, render: _Not provided._
-->
{{functional_scope_section}}

## Module Map
<!-- TEMPLATE-INSTRUCTION:
Extract major modules only when the user's context provides or clearly implies them.
For each module, include responsibility, main files, and notes when available.
If no module information is provided, render: _Not provided._
-->
{{module_map_section}}

## Project-Specific Agent Rules
<!-- TEMPLATE-INSTRUCTION:
Extract only repository-specific agent rules from the user's context.
Do not repeat general AI coding behavior rules from .agents/skills/karpathy-guidelines/SKILL.md or user collaboration protocol rules from docs/ai-guidelines/COLLABORATION-PROTOCOL.md.
If no project-specific rules are provided, render: _Not provided._
-->
{{project_specific_agent_rules}}
