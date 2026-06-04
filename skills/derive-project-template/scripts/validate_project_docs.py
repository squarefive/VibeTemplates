import argparse
import re
from pathlib import Path


REQUIRED_FILES = [
    Path("AGENTS.md"),
    Path("README.md"),
    Path("docs/ai-guidelines/AI-COLLABORATION.md"),
]

REQUIRED_AGENTS_SECTIONS = [
    "# AGENTS.md",
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
    guideline = (
        root / "docs" / "ai-guidelines" / "AI-COLLABORATION.md"
    ).read_text(encoding="utf-8")

    for section in REQUIRED_AGENTS_SECTIONS:
        if section not in agents:
            errors.append(f"AGENTS.md missing section: {section}")

    for section in REQUIRED_README_SECTIONS:
        if section not in readme:
            errors.append(f"README.md missing section: {section}")

    for relative, content in {
        "AGENTS.md": agents,
        "README.md": readme,
        "docs/ai-guidelines/AI-COLLABORATION.md": guideline,
    }.items():
        if "TEMPLATE-INSTRUCTION" in content:
            errors.append(f"{relative} contains TEMPLATE-INSTRUCTION")
        if PLACEHOLDER_RE.search(content):
            errors.append(f"{relative} contains unresolved placeholder")

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
