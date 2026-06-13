# Repository Guidelines

## Project Background & Positioning

VibeTemplates maintains reusable Codex skills that help other people initialize shared project foundations. The primary skill should make common setup repeatable: generating documentation templates, adding agent collaboration guidance, and configuring supporting MCP tools where appropriate.

This is not an application repository. Treat it as a source repository for portable skills, templates, and conventions. When extending it, first consider how the change can be exposed for others to use safely and clearly. Prefer reusable inputs, documented defaults, and examples that avoid machine-specific assumptions.

## Project Structure & Module Organization

This repository contains reusable Codex skills, documentation templates, tests, and a local MCP tool.

- `skills/derive-project-template/`: main Codex skill for generating project documentation.
- `skills/derive-project-template/assets/templates/`: Markdown templates and helper files copied into target projects.
- `skills/derive-project-template/scripts/`: generation and validation scripts.
- `tests/`: repository-level pytest coverage for template generation and validation behavior.
- `tools/code-readability-mcp/`: Python MCP server for readability diagnostics, with source under `src/code_readability_mcp/` and tests under `tests/`.
- `.agents/skills/karpathy-guidelines/`: bundled guidance mirrored into generated projects.

## Build, Test, and Development Commands

Run all root tests:

```bash
python3 -m pytest -q
```

Generate docs from a JSON config:

```bash
python3 skills/derive-project-template/scripts/init_project_docs.py --config config.json --output /path/to/project
```

Validate generated docs:

```bash
python3 skills/derive-project-template/scripts/validate_project_docs.py --path /path/to/project
```

Test the MCP tool separately:

```bash
cd tools/code-readability-mcp
python3 -m pytest -q
```

## Coding Style & Naming Conventions

Use Python 3 syntax with 4-space indentation, explicit names, and small functions. Prefer `pathlib.Path`, structured data over string scraping, and clear script entry points. Test files use `test_*.py`; Python modules use lowercase snake_case names.

## Testing Guidelines

The project uses `pytest`. Add or update tests whenever changing template output, validation rules, script behavior, or MCP analyzer logic. Keep tests focused on observable behavior: generated files, validation results, CLI exit codes, and structured MCP outputs.

## Commit & Pull Request Guidelines

Recent history uses concise prefixed commit subjects such as `feat: add code readability mcp`, `docs: add project readme`, and `merge: ...`. Follow that style with an imperative, lower-case summary.

Pull requests should describe the change, note affected templates/scripts/tools, include test results, and mention any generated-file impact. Link related issues when available. Screenshots are only needed for rendered documentation or UI-facing changes.

## Security & Configuration Tips

Do not hard-code machine-specific paths unless marked as examples. Avoid committing virtual environments, caches, credentials, or generated MCP egg-info artifacts unless intentionally required.
