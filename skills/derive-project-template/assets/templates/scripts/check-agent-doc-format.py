#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FRONTMATTER_FIELDS = [
    "module",
    "title",
    "language",
    "agent_type",
    "last_updated",
]

REQUIRED_SECTIONS = [
    "## 1. Agent 定位与能力边界",
    "## 2. Harness 架构与代码边界",
    "## 3. 可调用工具与工具契约",
    "## 4. 上下文来源与记忆边界",
    "## 5. 核心业务流",
    "## 6. 数据模型",
    "## 7. 失败模式与降级策略",
    "## 8. 测试要求",
    "## 9. 变更记录",
]

REQUIRED_KEY_AREAS = [
    "### 3.1 工具列表",
    "### 3.2 工具契约",
    "## 6. 数据模型",
    "## 7. 失败模式与降级策略",
    "## 8. 测试要求",
    "## 9. 变更记录",
]

PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_frontmatter(content: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not content.startswith("---\n"):
        return {}, ["missing YAML frontmatter"]

    end = content.find("\n---\n", 4)
    if end == -1:
        return {}, ["YAML frontmatter is not closed"]

    fields: dict[str, str] = {}
    for line in content[4:end].splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields, errors


def check_frontmatter(content: str) -> list[str]:
    fields, errors = extract_frontmatter(content)
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in fields:
            errors.append(f"missing frontmatter field: {field}")

    last_updated = fields.get("last_updated", "")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", last_updated):
        errors.append("frontmatter field last_updated must match YYYY-MM-DD")

    for field in REQUIRED_FRONTMATTER_FIELDS:
        value = fields.get(field, "")
        if not value:
            errors.append(f"frontmatter field {field} must not be empty")
    return errors


def check_agent_doc(path: Path) -> list[str]:
    content = read_text(path)
    errors = check_frontmatter(content)

    for marker in ["文档定位", "AI 阅读契约"]:
        if marker not in content:
            errors.append(f"missing required marker: {marker}")

    for section in REQUIRED_SECTIONS:
        if section not in content:
            errors.append(f"missing required section: {section}")

    for area in REQUIRED_KEY_AREAS:
        if area not in content:
            errors.append(f"missing required key area: {area}")

    if not re.search(r"^# .+ Agent 开发上下文$", content, re.MULTILINE):
        errors.append("missing H1 title matching '# ... Agent 开发上下文'")

    if PLACEHOLDER_RE.search(content):
        errors.append("template placeholders must be filled before committing")
    return errors


def resolve_targets(targets: list[str], root: Path) -> tuple[list[Path], list[str]]:
    files: list[Path] = []
    errors: list[str] = []

    for target in targets:
        path = (root / target).resolve() if not Path(target).is_absolute() else Path(target)
        if path.is_dir():
            markdown_files = sorted(path.glob("*.md"))
            if not markdown_files:
                print(f"[info] no markdown files found in {rel(path, root)}")
            files.extend(markdown_files)
        elif path.is_file() and path.suffix == ".md":
            files.append(path)
        else:
            errors.append(f"target is not a markdown file or directory: {target}")
    return sorted(set(files)), errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check Agent development context docs format."
    )
    parser.add_argument(
        "targets",
        nargs="*",
        default=["docs/agents"],
        help="Markdown files or directories to check. Defaults to docs/agents/*.md.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    files, errors = resolve_targets(args.targets, root)
    checked = 0

    for path in files:
        checked += 1
        path_errors = check_agent_doc(path)
        if path_errors:
            errors.extend(f"{rel(path, root)}: {error}" for error in path_errors)
            print(f"[fail] {rel(path, root)}")
        else:
            print(f"[pass] {rel(path, root)}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"\nChecked {checked} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
