# Code Readability MCP

This MCP server provides cross-repository diagnostics for code readability rules.

The first version supports Python and exposes three tools:

- `explain_code_readability_rules`: Return the active readability rules.
- `list_code_readability_targets`: Discover Python files with `changed-files` or `all` mode.
- `analyze_code_readability`: Analyze explicit files and return structured findings.

## Rules

The Python analyzer checks docstring coverage, class documentation, class member documentation, semantic names, magic numbers, type annotations, silent exception handlers, function length, and nesting depth.

## Codex Configuration

Configure the MCP server in your local Codex configuration with the path that matches your machine. The template skill should remind users before adding local MCP configuration because paths differ across machines.

Example command target:

```bash
code-readability-mcp
```

## Development

Run checks from this directory:

```bash
python3 -m pytest -q
```

The analyzer is designed so the core logic can be tested without the MCP SDK installed.
