# AGENTS.md

## AGENTS.md Role

This file is the AI coding work entry point for this repository and the
top-level index for local documentation and collaboration rules.

It answers only these questions:

- which collaboration rules must be read before starting work
- which development documents must be read for specific task types
- what responsibility each linked document carries

It must not contain full Agent design boundaries, code implementation plans,
single-task plans, temporary decisions, or work progress.

Keep this file short, stable, and scannable. Long-form protocols, design rules,
code maps, Agent context, and detailed implementation notes belong in dedicated
documents linked from this file.

## Context Loading Rules

### Collaboration Protocol

- Read when: planning, local file changes, persistent commands, branch changes,
  merges, commits, or when the user asks to follow the collaboration protocol.
- Used for: change control, plan shape, branch strategy, execution confirmation,
  and commit preferences.
- Does not replace: project facts, code structure, design rules, or Agent
  development boundaries.

Read: `docs/ai-guidelines/COLLABORATION-PROTOCOL.md`

### Design Principles

- Read when: adding modules, changing dependencies, introducing abstractions,
  changing layer boundaries, or making architecture-level decisions.
- Used for: software design constraints, dependency direction, layering, and
  abstraction decisions.
- Does not replace: the current codebase map or project-specific module facts.

Read: `docs/engineering-guidelines/DESIGN-PRINCIPLES.md`

### Codebase Map

- Read when: code navigation, file placement, module responsibility checks,
  source structure changes, tests, verification, or debugging.
- Used for: current directories, modules, file responsibilities, and entry
  points.
- Does not replace: Agent capability boundaries or design principles.

Read: `docs/architecture/codebase-map.md`

After changing the codebase map, run:

```bash
python3 scripts/check-codebase-map-format.py
```

### Agent Development Context

- Read when: implementing, modifying, or refactoring a specific Agent.
- Used for: Agent role boundaries, tool contracts, data boundaries, workflows,
  failure modes, and testing requirements.
- Does not replace: task plans, collaboration protocol, codebase map, or runtime
  prompts.

Read: `docs/agents/<agent>.md`

### Agent Context Template

- Read when: creating a new Agent development context document, modifying the
  shared Agent document structure, or upgrading the Agent context template.
- Used for: stable Agent context document structure.
- Does not replace: a concrete Agent development context document or a
  task-specific implementation plan.

Read: `docs/agents/<agent>.md` first for existing Agent work. Read the template
only for Agent document creation or template upgrades.

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
