"""Structured result models for code readability diagnostics."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal


Severity = Literal["error", "warning"]


@dataclass(frozen=True)
class RuleDescription:
    """Describe one readability rule returned by the rules tool.

    Attributes:
        id: Stable rule identifier.
        severity: Rule severity returned to callers.
        description: Human-readable rule explanation.
    """

    id: str
    severity: Severity
    description: str

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-ready rule description.

        Inputs:
            None.

        Outputs:
            A dictionary containing rule id, severity, and description.

        Side Effects:
            None.
        """
        return asdict(self)


@dataclass(frozen=True)
class ReadabilityFinding:
    """Describe one code readability violation.

    Attributes:
        file: Repository-relative source file path.
        line: One-based line number where the finding applies.
        rule: Stable rule identifier that produced the finding.
        severity: Finding severity returned to callers.
        message: Human-readable diagnostic message.
    """

    file: str
    line: int
    rule: str
    severity: Severity
    message: str

    def to_dict(self) -> dict[str, str | int]:
        """Return a JSON-ready finding.

        Inputs:
            None.

        Outputs:
            A dictionary containing file, line, rule, severity, and message.

        Side Effects:
            None.
        """
        return asdict(self)


@dataclass(frozen=True)
class ReadabilityAnalysisSummary:
    """Summarize one readability analysis run.

    Attributes:
        language: Programming language analyzed.
        files_checked: Number of source files analyzed.
        violations: Number of findings produced by the analyzer.
    """

    language: str
    files_checked: int
    violations: int

    def to_dict(self) -> dict[str, str | int]:
        """Return a JSON-ready analysis summary.

        Inputs:
            None.

        Outputs:
            A dictionary containing language, checked file count, and violation count.

        Side Effects:
            None.
        """
        return asdict(self)


@dataclass(frozen=True)
class ReadabilityAnalysisResult:
    """Bundle summary and findings for an analysis run.

    Attributes:
        summary: Aggregate information about the analysis run.
        findings: Individual readability diagnostics.
    """

    summary: ReadabilityAnalysisSummary
    findings: list[ReadabilityFinding]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready analysis result.

        Inputs:
            None.

        Outputs:
            A dictionary containing summary and finding dictionaries.

        Side Effects:
            None.
        """
        return {
            "summary": self.summary.to_dict(),
            "findings": [finding.to_dict() for finding in self.findings],
        }


@dataclass(frozen=True)
class ReadabilityTargetListResult:
    """Describe source files selected for readability analysis.

    Attributes:
        root: Repository root used for target discovery.
        language: Programming language selected for discovery.
        mode: Target discovery mode used to select files.
        files: Repository-relative source files selected for analysis.
    """

    root: str
    language: str
    mode: str
    files: list[str]

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready target list.

        Inputs:
            None.

        Outputs:
            A dictionary containing root, language, mode, and selected files.

        Side Effects:
            None.
        """
        return asdict(self)
