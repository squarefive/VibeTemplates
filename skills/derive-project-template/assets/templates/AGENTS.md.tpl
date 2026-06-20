# AGENTS.md

## AGENTS.md Role

This file provides durable project guidance for AI coding agents before they
start work in this repository.

Keep it small. Include only guidance that changes AI development decisions,
such as project purpose, functional scope, module boundaries, required reading
rules, build and test commands, and repository-specific constraints.

Do not use this file as a full documentation dump. Long-form protocols, design
rules, code maps, Agent context, and detailed implementation notes belong in
dedicated documents linked from this file.

## Context Loading Rules

Read `docs/ai-guidelines/COLLABORATION-PROTOCOL.md` before planning, local file
changes, persistent commands, branch changes, merges, or commits.

Read `docs/engineering-guidelines/DESIGN-PRINCIPLES.md` before adding modules,
changing dependencies, introducing abstractions, changing layer boundaries, or
making architecture-level decisions.

Read `docs/architecture/codebase-map.md` before code navigation, file placement,
module responsibility checks, or source structure changes.

Read `docs/agents/<agent>.md` before implementing, modifying, or refactoring a
specific Agent.

After changing the codebase map, run:

```bash
python3 scripts/check-codebase-map-format.py
```

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
