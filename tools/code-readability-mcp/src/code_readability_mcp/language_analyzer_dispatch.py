"""Dispatch readability analysis to the analyzer for the requested language."""

from __future__ import annotations

from .python_readability_analyzer import analyze_python_readability
from .readability_result_models import (
    ReadabilityAnalysisResult,
    ReadabilityAnalysisSummary,
)
from .readability_rule_registry import SUPPORTED_LANGUAGE


NO_FILES_CHECKED = 0
NO_VIOLATIONS = 0


def analyze_code_readability(
    root: str, language: str, files: list[str]
) -> dict[str, object]:
    """Analyze selected files with the requested language analyzer.

    Inputs:
        root: Repository root used to resolve file paths.
        language: Programming language identifier.
        files: Source files to analyze relative to root.

    Outputs:
        A dictionary containing analysis summary and structured findings.

    Side Effects:
        Reads source files. Does not modify files.
    """
    if not files:
        return {
            "summary": {
                "language": language,
                "files_checked": NO_FILES_CHECKED,
                "violations": NO_VIOLATIONS,
            },
            "findings": [],
            "error": "files must not be empty. Use list_code_readability_targets first.",
        }

    if language != SUPPORTED_LANGUAGE:
        result = ReadabilityAnalysisResult(
            summary=ReadabilityAnalysisSummary(
                language=language,
                files_checked=NO_FILES_CHECKED,
                violations=NO_VIOLATIONS,
            ),
            findings=[],
        )
        payload = result.to_dict()
        payload["error"] = (
            f"Unsupported language `{language}`. First version supports `python`."
        )
        return payload

    return analyze_python_readability(root, files).to_dict()
