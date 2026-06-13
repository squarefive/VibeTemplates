"""MCP server entry point for code readability diagnostics."""

from __future__ import annotations

from .language_analyzer_dispatch import analyze_code_readability as analyze_files
from .readability_rule_registry import explain_rules_for_language
from .readability_target_discovery import (
    DEFAULT_TARGET_MODE,
    list_code_readability_targets as discover_targets,
)

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # pragma: no cover - depends on optional MCP SDK installation.
    FastMCP = None  # type: ignore[assignment]


SERVER_NAME = "code-readability-mcp"
EXIT_SUCCESS = 0
EXIT_MISSING_MCP_SDK = 1


def build_mcp_server() -> object:
    """Build the MCP server and register code readability tools.

    Inputs:
        None.

    Outputs:
        A configured MCP server instance.

    Side Effects:
        Registers MCP tools with the server instance.
    """
    if FastMCP is None:
        raise RuntimeError("The optional MCP SDK is not installed.")

    server = FastMCP(SERVER_NAME)
    server.tool()(explain_code_readability_rules)
    server.tool()(list_code_readability_targets)
    server.tool()(analyze_code_readability)
    return server


async def explain_code_readability_rules(language: str) -> dict[str, object]:
    """Explain the active code readability rules for a language.

    Use this tool before writing or reviewing code when you need to know the
    current readability requirements. It returns the rules that the analyzer
    enforces, including required docstring sections, naming expectations,
    magic-number policy, type annotation requirements, and complexity limits.

    Inputs:
        language: Programming language identifier. The first version supports
            "python".

    Outputs:
        A dictionary containing rule identifiers, severities, and descriptions.

    Side Effects:
        None.
    """
    return explain_rules_for_language(language)


async def list_code_readability_targets(
    root: str, language: str, mode: str = DEFAULT_TARGET_MODE
) -> dict[str, object]:
    """List source files that should be checked for code readability.

    Use this tool before analysis when you want Codex to discover files for
    either the current Git changes or all Python files under a repository.
    It does not analyze code; it only returns a stable file list.

    Inputs:
        root: Repository root used to discover source files.
        language: Programming language identifier. The first version supports
            "python".
        mode: Target discovery mode. Supported values are "changed-files" and
            "all". Defaults to "changed-files".

    Outputs:
        A dictionary containing root, language, mode, and selected files.

    Side Effects:
        Reads the filesystem and may call Git read-only commands. Does not
        modify files.
    """
    return discover_targets(root=root, language=language, mode=mode)


async def analyze_code_readability(
    root: str, language: str, files: list[str]
) -> dict[str, object]:
    """Analyze selected source files for code readability violations.

    Use this tool after writing, modifying, or reviewing code. Pass explicit
    files from user context or from list_code_readability_targets. It checks
    docstring coverage, naming, magic numbers, type annotations, exception
    handling, function length, and nesting depth.

    Inputs:
        root: Repository root used to resolve file paths.
        language: Programming language identifier. The first version supports
            "python".
        files: Source files to inspect, relative to root. Must not be empty.

    Outputs:
        A dictionary with a summary and structured findings. Each finding
        includes file, line, rule, severity, and message.

    Side Effects:
        Reads source files only. Does not modify files.
    """
    return analyze_files(root=root, language=language, files=files)


def main() -> int:
    """Run the MCP server command.

    Inputs:
        None.

    Outputs:
        Process exit code.

    Side Effects:
        Starts the MCP server when the optional MCP SDK is installed.
    """
    server = build_mcp_server()
    server.run()  # type: ignore[attr-defined]
    return EXIT_SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())
