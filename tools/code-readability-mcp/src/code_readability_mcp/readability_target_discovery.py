"""Discover source files for code readability analysis."""

from __future__ import annotations

import subprocess
from pathlib import Path

from .readability_result_models import ReadabilityTargetListResult
from .readability_rule_registry import SUPPORTED_LANGUAGE


DEFAULT_TARGET_MODE = "changed-files"
ALL_TARGET_MODE = "all"
CHANGED_FILES_TARGET_MODE = "changed-files"
PYTHON_SUFFIX = ".py"
EXCLUDED_DIRECTORY_NAMES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".coverage",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}


def list_code_readability_targets(
    root: str, language: str, mode: str = DEFAULT_TARGET_MODE
) -> dict[str, object]:
    """Return files selected for readability analysis.

    Inputs:
        root: Repository root used to discover files.
        language: Programming language identifier.
        mode: Target discovery mode. Supported values are changed-files and all.

    Outputs:
        A dictionary containing selected files relative to root.

    Side Effects:
        Reads the filesystem and may call Git. Does not modify files.
    """
    root_path = Path(root).resolve()
    selected_mode = mode or DEFAULT_TARGET_MODE

    if language != SUPPORTED_LANGUAGE:
        return {
            "root": str(root_path),
            "language": language,
            "mode": selected_mode,
            "files": [],
            "error": f"Unsupported language `{language}`. First version supports `python`.",
        }

    if selected_mode == ALL_TARGET_MODE:
        files = discover_all_python_files(root_path)
    elif selected_mode == CHANGED_FILES_TARGET_MODE:
        files = discover_changed_python_files(root_path)
    else:
        return {
            "root": str(root_path),
            "language": language,
            "mode": selected_mode,
            "files": [],
            "error": f"Unsupported target discovery mode `{selected_mode}`.",
        }

    return ReadabilityTargetListResult(
        root=str(root_path), language=language, mode=selected_mode, files=files
    ).to_dict()


def discover_all_python_files(root: Path) -> list[str]:
    """Discover Python files under root while skipping generated and dependency directories.

    Inputs:
        root: Repository root to scan.

    Outputs:
        Python file paths relative to root.

    Side Effects:
        Reads directory entries. Does not modify files.
    """
    files = []
    for path in root.rglob(f"*{PYTHON_SUFFIX}"):
        if _has_excluded_directory(path.relative_to(root)):
            continue
        files.append(path.relative_to(root).as_posix())
    return sorted(files)


def discover_changed_python_files(root: Path) -> list[str]:
    """Discover changed Python files from staged, unstaged, and untracked Git state.

    Inputs:
        root: Repository root where Git commands should run.

    Outputs:
        Changed Python file paths relative to root.

    Side Effects:
        Calls Git read-only commands. Does not modify files.
    """
    changed_files = set()
    for command in (
        ["git", "diff", "--name-only"],
        ["git", "diff", "--cached", "--name-only"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ):
        changed_files.update(_run_git_file_list(root, command))

    return sorted(
        path
        for path in changed_files
        if path.endswith(PYTHON_SUFFIX)
        and not _has_excluded_directory(Path(path))
        and (root / path).exists()
    )


def _run_git_file_list(root: Path, command: list[str]) -> list[str]:
    """Run a Git command that returns file paths."""
    result = subprocess.run(
        command,
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _has_excluded_directory(path: Path) -> bool:
    """Return whether a path contains an excluded directory name."""
    return any(part in EXCLUDED_DIRECTORY_NAMES for part in path.parts)
