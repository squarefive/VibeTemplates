# VibeTemplates

## What It Is

This repository contains reusable Codex skills and templates for deriving project documentation from provided project context.

The current skill is `derive-project-template`.

## What It Generates

For a normal project, the skill generates:

- `AGENTS.md`
- `README.md`
- `docs/architecture/codebase-map.md`
- `docs/engineering-guidelines/DESIGN-PRINCIPLES.md`
- `docs/ai-guidelines/COLLABORATION-PROTOCOL.md`
- `.agents/skills/karpathy-guidelines/SKILL.md`
- `scripts/check-codebase-map-format.py`

The generated `karpathy-guidelines` skill provides general AI coding behavior rules for Codex. This repository also includes the same skill under `.agents/skills/karpathy-guidelines/SKILL.md`.

The generated codebase map gives AI coding tools a stable entry point for
source directories, modules, and file responsibilities. The generated checker
validates the map format after documentation or source structure changes.

The generated design principles document gives AI coding agents stable software
design constraints for module boundaries, dependency direction, layering, and
abstraction decisions.

## Optional VS Code Markdown Translation Extension

The `derive-project-template` skill bundles an optional local VS Code Markdown
translation extension artifact under:

```text
skills/derive-project-template/assets/tools/vscode/
```

When the skill runs locally and the VS Code `code` CLI is available, Codex can
install the bundled VSIX if the extension is not already installed. The skill
does not rebuild the extension, run `npm install`, or download extension assets.

After installation, configure the LLM provider in VS Code Settings with
`mdTranslate.baseUrl`, `mdTranslate.apiKey`, `mdTranslate.model`,
`mdTranslate.targetLanguage`, `mdTranslate.maxSectionChars`, and
`mdTranslate.enableCache`.

## Code Readability MCP

This repository includes `tools/code-readability-mcp`, a reusable MCP server for cross-repository code readability diagnostics.

The first version supports Python and provides three tools:

- `explain_code_readability_rules`
- `list_code_readability_targets`
- `analyze_code_readability`

Use it when you want Codex to diagnose docstring coverage, semantic naming, magic numbers, type annotations, exception handling, function length, and nesting depth across repositories.

For an Agent development project, when `agent_module_name` and `agent_chinese_name` are provided, it also generates:

- `docs/agents/<agent>.md`
- `scripts/check-agent-doc-format.py`

## How To Use

Ask Codex to use the skill with a prompt like this:

```text
Use the derive-project-template skill to initialize project documentation for this repository.

Project context:
Design and implement a knowledge-base Agent for scientific literature management. The system integrates Zotero and Obsidian to support automatic literature metadata synchronization, automatic Markdown note generation, abstract-level AI pre-screening, human review workflows, and deep PDF reading. It uses a multi-stage Agent workflow to orchestrate PDF parsing, section recognition, goal-driven reading, structured information extraction, and knowledge-base writeback, improving the efficiency of literature screening, close reading, and knowledge consolidation.

This is an Agent development project.
Agent module: research_literature_knowledge_agent
Agent Chinese name: 科研文献知识库
Language: Python
Agent type: Workflow Agent

Extract only information that is available from this prompt and the repository. Use _Not provided._ for missing fields. Run validation before reporting completion.
```

You can also run the scripts directly from a prepared config:

```bash
python3 skills/derive-project-template/scripts/init_project_docs.py --config config.json --output /path/to/target-project
python3 skills/derive-project-template/scripts/validate_project_docs.py --path /path/to/target-project
```

Field rules and generation details live in `skills/derive-project-template/SKILL.md`.

## Development

Run tests with:

```bash
python3 -m pytest -q
```

If `pytest` is not installed, install it in the local Python environment or run script-level generation and validation checks manually.
