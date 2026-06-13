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

## MCP Inspector Manual Testing

Use MCP Inspector to manually test this local MCP server over STDIO.

### 1. Install with MCP support

From this directory, create or use a Python 3.11+ environment and install the
package with its optional MCP dependency:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[mcp]'
```

### 2. Start MCP Inspector

```bash
npx @modelcontextprotocol/inspector
```

Open the local Inspector URL printed by the command.

### 3. Configure the server

In MCP Inspector, use these settings:

```text
Transport Type: STDIO
Command: /absolute/path/to/code-readability-mcp/.venv/bin/code-readability-mcp
Arguments: leave empty
```

Example for this repository on this machine:

```text
Transport Type: STDIO
Command: /Users/squarefive/Developer/personal/VibeTemplates/tools/code-readability-mcp/.venv/bin/code-readability-mcp
Arguments:
```

Click **Connect**, open the **Tools** tab, then click **List Tools**.

If you installed the package in a temporary or external environment, use that
environment's `code-readability-mcp` executable as the command instead.

### 4. Demo tool calls

#### explain_code_readability_rules

```json
{
  "language": "python"
}
```

#### list_code_readability_targets

```json
{
  "root": "/Users/squarefive/Developer/personal/VibeTemplates/tools/code-readability-mcp",
  "language": "python",
  "mode": "all"
}
```

#### analyze_code_readability

```json
{
  "root": "/Users/squarefive/Developer/personal/VibeTemplates/tools/code-readability-mcp",
  "language": "python",
  "files": ["src/code_readability_mcp/mcp_server.py"]
}
```

### Notes

- Use Python 3.11 or newer.
- Some macOS system `python3` installations are older than the project
  requirement.
- If `code-readability-mcp` is not found, point Inspector at the executable
  inside the virtual environment.

## Development

Run checks from this directory:

```bash
python3 -m pytest -q
```

The analyzer is designed so the core logic can be tested without the MCP SDK installed.
