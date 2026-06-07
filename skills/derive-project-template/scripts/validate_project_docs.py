import argparse
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_FILES = [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("docs/ai-guidelines/AI-CODING-BEHAVIOR.md"),
    Path("docs/ai-guidelines/COLLABORATION-PROTOCOL.md"),
]

REQUIRED_AGENTS_SECTIONS = [
    "# AGENTS.md",
    "## Guideline Index",
    "## Project Context",
    "## Functional Scope And Completeness",
    "## Module Map",
    "## Project-Specific Agent Rules",
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

REQUIRED_GUIDELINE_LINKS = [
    "docs/ai-guidelines/AI-CODING-BEHAVIOR.md",
    "docs/ai-guidelines/COLLABORATION-PROTOCOL.md",
]

AGENT_INDEX_SECTION = "## Agent Development Context Index"
AGENT_CHECKER = Path("scripts/check-agent-doc-format.py")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate generated project documentation structure."
    )
    parser.add_argument("--path", required=True, help="Target project directory.")
    return parser.parse_args()


def collect_errors(root: Path) -> list[str]:
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).exists():
            errors.append(f"Missing required file: {relative.as_posix()}")

    if errors:
        return errors

    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    readme = (root / "README.md").read_text(encoding="utf-8")
    contents = {
        relative.as_posix(): (root / relative).read_text(encoding="utf-8")
        for relative in REQUIRED_FILES
    }
    agents = contents["AGENTS.md"]
    readme = contents["README.md"]

    for section in REQUIRED_AGENTS_SECTIONS:
        if section not in agents:
            errors.append(f"AGENTS.md missing section: {section}")

    for guideline_link in REQUIRED_GUIDELINE_LINKS:
        if guideline_link not in agents:
            errors.append(f"AGENTS.md missing guideline link: {guideline_link}")

    for section in REQUIRED_README_SECTIONS:
        if section not in readme:
            errors.append(f"README.md missing section: {section}")

    for relative, content in contents.items():
        if "TEMPLATE-INSTRUCTION" in content:
            errors.append(f"{relative} contains TEMPLATE-INSTRUCTION")
        if PLACEHOLDER_RE.search(content):
            errors.append(f"{relative} contains unresolved placeholder")

    agent_docs = sorted((root / "docs" / "agents").glob("*.md"))
    if agent_docs:
        if AGENT_INDEX_SECTION not in agents:
            errors.append(f"AGENTS.md missing section: {AGENT_INDEX_SECTION}")

        for agent_doc in agent_docs:
            relative = agent_doc.relative_to(root).as_posix()
            if relative not in agents:
                errors.append(f"AGENTS.md missing agent context link: {relative}")

        checker = root / AGENT_CHECKER
        if not checker.exists():
            errors.append(f"Missing agent doc checker: {AGENT_CHECKER.as_posix()}")
        else:
            result = subprocess.run(
                [sys.executable, str(checker), *[str(path) for path in agent_docs]],
                cwd=root,
                text=True,
                capture_output=True,
            )
            if result.returncode != 0:
                details = "\n".join(
                    line
                    for line in (result.stdout + result.stderr).splitlines()
                    if line.strip()
                )
                errors.append(f"Agent doc format check failed:\n{details}")

    return errors


def main() -> int:
    args = parse_args()
    errors = collect_errors(Path(args.path))
    if errors:
        print("validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
