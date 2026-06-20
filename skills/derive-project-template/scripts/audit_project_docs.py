from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REQUIRED_FILES = [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("docs/architecture/codebase-map.md"),
    Path("docs/engineering-guidelines/DESIGN-PRINCIPLES.md"),
    Path("docs/ai-guidelines/COLLABORATION-PROTOCOL.md"),
    Path(".agents/skills/karpathy-guidelines/SKILL.md"),
    Path("scripts/check-codebase-map-format.py"),
]

REQUIRED_AGENTS_SECTIONS = [
    "# AGENTS.md",
    "## AGENTS.md Role",
    "## Context Loading Rules",
    "## Project Context",
    "## Functional Scope And Completeness",
    "## Module Map",
    "## Project-Specific Agent Rules",
]

REQUIRED_AGENTS_LINKS = [
    "docs/ai-guidelines/COLLABORATION-PROTOCOL.md",
    "docs/engineering-guidelines/DESIGN-PRINCIPLES.md",
    "docs/architecture/codebase-map.md",
]

REQUIRED_README_SECTIONS = [
    "# ",
    "## Overview",
    "## Features",
    "## Project Structure",
    "## Getting Started",
    "## Development",
]

PLACEHOLDER_RE = re.compile(r"{{[^}]+}}")
AGENT_CHECKER = Path("scripts/check-agent-doc-format.py")
CODEBASE_MAP_CHECKER = Path("scripts/check-codebase-map-format.py")
STATUS_OK = 0
STATUS_PARTIAL = 1
STATUS_FAILED = 2


@dataclass(frozen=True)
class AuditFinding:
    """One project documentation audit finding.

    Attributes:
        category: Finding category, such as missing, structure, or invalid.
        path: Repository-relative file or directory path.
        message: Human-readable audit issue.
        suggested_action: Incremental repair action for this issue.
    """

    category: str
    path: str
    message: str
    suggested_action: str


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Audit project documentation against derive-project-template expectations."
    )
    parser.add_argument("--path", required=True, help="Target project directory.")
    return parser.parse_args()


def _read_existing_text(root: Path, relative: Path) -> str | None:
    """Read a target file when it exists."""
    path = root / relative
    if not path.exists() or not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


def _collect_existence_findings(root: Path) -> tuple[list[str], list[AuditFinding]]:
    """Collect required-file existence findings."""
    existing = []
    findings = []
    for relative in REQUIRED_FILES:
        if (root / relative).exists():
            existing.append(relative.as_posix())
        else:
            relative_text = relative.as_posix()
            findings.append(
                AuditFinding(
                    "missing",
                    relative_text,
                    f"Missing required file: `{relative_text}`",
                    f"Add `{relative_text}` from the bundled template.",
                )
            )
    return existing, findings


def _collect_text_structure_findings(root: Path) -> list[AuditFinding]:
    """Collect section, link, and placeholder findings."""
    findings = []
    agents = _read_existing_text(root, Path("AGENTS.md"))
    if agents is not None:
        findings.extend(
            _check_required_sections(
                "AGENTS.md",
                agents,
                REQUIRED_AGENTS_SECTIONS,
                "Add the missing section while preserving existing project context.",
            )
        )
        findings.extend(
            _check_required_links(
                "AGENTS.md",
                agents,
                REQUIRED_AGENTS_LINKS,
                "Add the missing context loading rule or link; keep existing guidance.",
            )
        )
        findings.extend(_check_template_artifacts("AGENTS.md", agents))

    readme = _read_existing_text(root, Path("README.md"))
    if readme is not None:
        findings.extend(
            _check_required_sections(
                "README.md",
                readme,
                REQUIRED_README_SECTIONS,
                "Add the missing section while preserving existing README content.",
            )
        )
        findings.extend(_check_template_artifacts("README.md", readme))

    for relative in REQUIRED_FILES:
        content = _read_existing_text(root, relative)
        if content is not None and relative.as_posix() not in {"AGENTS.md", "README.md"}:
            findings.extend(_check_template_artifacts(relative.as_posix(), content))

    return findings


def _check_required_sections(
    path: str, content: str, sections: list[str], suggested_action: str
) -> list[AuditFinding]:
    """Check whether all required section markers exist."""
    findings = []
    for section in sections:
        if section not in content:
            findings.append(
                AuditFinding(
                    "structure",
                    path,
                    f"Missing section: `{section}`",
                    suggested_action,
                )
            )
    return findings


def _check_required_links(
    path: str, content: str, links: list[str], suggested_action: str
) -> list[AuditFinding]:
    """Check whether all required document links exist."""
    findings = []
    for link in links:
        if link not in content:
            findings.append(
                AuditFinding(
                    "structure",
                    path,
                    f"Missing required link: `{link}`",
                    suggested_action,
                )
            )
    return findings


def _check_template_artifacts(path: str, content: str) -> list[AuditFinding]:
    """Check for unresolved template-only content."""
    findings = []
    if "TEMPLATE-INSTRUCTION" in content:
        findings.append(
            AuditFinding(
                "structure",
                path,
                "Contains TEMPLATE-INSTRUCTION marker.",
                "Remove template-only instructions while preserving project content.",
            )
        )
    if PLACEHOLDER_RE.search(content):
        findings.append(
            AuditFinding(
                "structure",
                path,
                "Contains unresolved template placeholder.",
                "Fill the unresolved placeholder with project-specific content or `_Not provided._`.",
            )
        )
    return findings


def _collect_checker_findings(root: Path) -> list[AuditFinding]:
    """Collect findings from generated checker scripts."""
    return [
        *_collect_codebase_map_checker_findings(root),
        *_collect_agent_checker_findings(root),
    ]


def _collect_codebase_map_checker_findings(root: Path) -> list[AuditFinding]:
    """Collect codebase map checker findings."""
    findings = []
    if (root / CODEBASE_MAP_CHECKER).exists():
        result = _run_checker(root, [sys.executable, str(root / CODEBASE_MAP_CHECKER)])
        if result:
            findings.append(
                AuditFinding(
                    "invalid",
                    "docs/architecture/codebase-map.md",
                    f"Codebase map checker failed: {result}",
                    "Modify `docs/architecture/codebase-map.md` incrementally to satisfy the checker.",
                )
            )
    return findings


def _collect_agent_checker_findings(root: Path) -> list[AuditFinding]:
    """Collect Agent document checker and AGENTS.md link findings."""
    findings = []
    agent_docs = sorted((root / "docs" / "agents").glob("*.md"))
    if agent_docs:
        agents = _read_existing_text(root, Path("AGENTS.md")) or ""
        if not (root / AGENT_CHECKER).exists():
            findings.append(
                AuditFinding(
                    "missing",
                    AGENT_CHECKER.as_posix(),
                    f"Missing required file: `{AGENT_CHECKER.as_posix()}`",
                    f"Add `{AGENT_CHECKER.as_posix()}` because Agent context documents exist.",
                )
            )
        else:
            command = [
                sys.executable,
                str(root / AGENT_CHECKER),
                *[str(path) for path in agent_docs],
            ]
            result = _run_checker(root, command)
            if result:
                findings.append(
                    AuditFinding(
                        "invalid",
                        "docs/agents",
                        f"Agent document checker failed: {result}",
                        "Modify the existing Agent document structure incrementally to satisfy the checker.",
                    )
                )

        for agent_doc in agent_docs:
            relative = agent_doc.relative_to(root).as_posix()
            if relative not in agents:
                findings.append(
                    AuditFinding(
                        "structure",
                        "AGENTS.md",
                        f"Missing Agent context link: `{relative}`",
                        "Add the missing Agent context link; keep existing AGENTS.md content.",
                    )
                )
    return findings


def _run_checker(root: Path, command: list[str]) -> str:
    """Run a generated checker and return compact failure details."""
    result = subprocess.run(command, cwd=root, text=True, capture_output=True)
    if result.returncode == STATUS_OK:
        return ""
    lines = [
        line.strip()
        for line in (result.stdout + result.stderr).splitlines()
        if line.strip()
    ]
    return "; ".join(lines)


def _group_findings(
    findings: list[AuditFinding], category: str
) -> dict[str, list[AuditFinding]]:
    """Group findings in one category by path."""
    grouped: dict[str, list[AuditFinding]] = {}
    for finding in findings:
        if finding.category != category:
            continue
        grouped.setdefault(finding.path, []).append(finding)
    return grouped


def _render_audit_report(
    root: Path, existing: list[str], findings: list[AuditFinding], status: str
) -> str:
    """Render the fixed Markdown audit report."""
    lines = [
        "# Project Documentation Audit",
        "",
        f"Path: {root}",
        "",
        "Audit Result:",
        f"- status: {status}",
        "",
        "Existing:",
    ]
    lines.extend(_render_flat_items(existing))
    lines.extend(["", "Missing:"])
    lines.extend(_render_grouped_findings(_group_findings(findings, "missing")))
    lines.extend(["", "Structure Mismatches:"])
    lines.extend(_render_grouped_findings(_group_findings(findings, "structure")))
    lines.extend(["", "Invalid:"])
    lines.extend(_render_grouped_findings(_group_findings(findings, "invalid")))
    lines.extend(["", "Manual Review:", "- None", "", "Incremental Update Scope:", ""])
    lines.extend(_render_update_scope(findings))
    return "\n".join(lines) + "\n"


def _render_flat_items(items: list[str]) -> list[str]:
    """Render a flat list section."""
    if not items:
        return ["- None"]
    return [f"- `{item}`" for item in items]


def _render_grouped_findings(grouped: dict[str, list[AuditFinding]]) -> list[str]:
    """Render findings grouped by path."""
    if not grouped:
        return ["- None"]
    lines = []
    for path, findings in grouped.items():
        lines.append(f"- `{path}`")
        for finding in findings:
            lines.append(f"  - {finding.message}")
    return lines


def _render_update_scope(findings: list[AuditFinding]) -> list[str]:
    """Render incremental add, modify, and delete scope."""
    add_actions = [
        finding for finding in findings if finding.category == "missing"
    ]
    modify_actions = [
        finding for finding in findings if finding.category in {"structure", "invalid"}
    ]

    lines = ["Add:"]
    lines.extend(_render_action_items(add_actions))
    lines.extend(["", "Modify:"])
    lines.extend(_render_action_items(modify_actions))
    lines.extend(["", "Delete:", "- None"])
    return lines


def _render_action_items(findings: list[AuditFinding]) -> list[str]:
    """Render de-duplicated incremental actions."""
    if not findings:
        return ["- None"]
    seen = set()
    lines = []
    for finding in findings:
        key = (finding.path, finding.suggested_action)
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"- `{finding.path}`: {finding.suggested_action}")
    return lines


def main() -> int:
    """Run the project documentation audit command.

    Inputs:
        None.

    Outputs:
        Process exit code.

    Side Effects:
        Reads project documentation files and prints an audit report.
    """
    args = _parse_args()
    root = Path(args.path).resolve()
    if not root.exists() or not root.is_dir():
        print(
            _render_audit_report(
                root,
                [],
                [
                    AuditFinding(
                        "invalid",
                        str(root),
                        "Audit target path does not exist or is not a directory.",
                        "Provide an existing project directory path.",
                    )
                ],
                "failed",
            ),
            end="",
        )
        return STATUS_FAILED

    existing, findings = _collect_existence_findings(root)
    findings.extend(_collect_text_structure_findings(root))
    findings.extend(_collect_checker_findings(root))
    status = "ok" if not findings else "partial"
    print(_render_audit_report(root, existing, findings, status), end="")
    return STATUS_OK if status == "ok" else STATUS_PARTIAL


if __name__ == "__main__":
    raise SystemExit(main())
