"""Python AST analyzer for code readability rules."""

from __future__ import annotations

import ast
from pathlib import Path

from .readability_result_models import (
    ReadabilityAnalysisResult,
    ReadabilityAnalysisSummary,
    ReadabilityFinding,
)
from .readability_rule_registry import (
    CLASS_DOCSTRING_RULE,
    CLASS_MEMBER_DOC_RULE,
    FILE_NOT_FOUND_RULE,
    FUNCTION_DOCSTRING_RULE,
    FUNCTION_TOO_LONG_RULE,
    MAX_FUNCTION_LINES,
    MAX_NESTING_DEPTH,
    NESTING_TOO_DEEP_RULE,
    NO_MAGIC_NUMBER_RULE,
    NO_SILENT_EXCEPTION_RULE,
    PUBLIC_FUNCTION_TYPE_ANNOTATIONS_RULE,
    SEMANTIC_FILE_NAME_RULE,
    SEMANTIC_FUNCTION_NAME_RULE,
    SUPPORTED_LANGUAGE,
)


LINE_COUNT_OFFSET = 1
FIRST_SEQUENCE_INDEX = 0
INITIAL_NESTING_DEPTH = 0
ROOT_NESTING_DEPTH = 0
GENERIC_FILE_STEMS = {"utils", "helpers", "manager", "common", "processor"}
GENERIC_FUNCTION_NAMES = {
    "do",
    "run",
    "handle",
    "process",
    "process_data",
    "do_stuff",
}
DOCSTRING_REQUIRED_SECTIONS = ("Inputs:", "Outputs:", "Side Effects:")
SELF_PARAMETER_NAMES = {"self", "cls"}


def analyze_python_readability(root: str, files: list[str]) -> ReadabilityAnalysisResult:
    """Analyze Python files for code readability rule violations.

    Inputs:
        root: Repository root used to resolve file paths.
        files: Python source files to analyze relative to root.

    Outputs:
        A readability analysis result containing a summary and findings.

    Side Effects:
        Reads Python source files. Does not modify files.
    """
    root_path = Path(root).resolve()
    findings = []

    for relative_file in files:
        file_path = root_path / relative_file
        findings.extend(_analyze_file(root_path, file_path))

    return ReadabilityAnalysisResult(
        summary=ReadabilityAnalysisSummary(
            language=SUPPORTED_LANGUAGE,
            files_checked=len(files),
            violations=len(findings),
        ),
        findings=findings,
    )


def _analyze_file(root: Path, file_path: Path) -> list[ReadabilityFinding]:
    """Analyze one Python file and return findings."""
    relative_file = file_path.relative_to(root).as_posix()
    if not file_path.exists() or not file_path.is_file():
        return [
            _finding(
                relative_file,
                LINE_COUNT_OFFSET,
                FILE_NOT_FOUND_RULE,
                "error",
                f"File `{relative_file}` does not exist or is not readable.",
            )
        ]

    source = file_path.read_text(encoding="utf-8")
    findings = [_check_semantic_file_name(relative_file, file_path)]
    findings = [finding for finding in findings if finding is not None]

    try:
        tree = ast.parse(source, filename=relative_file)
    except SyntaxError as exc:
        return findings + [
            _finding(relative_file, exc.lineno or LINE_COUNT_OFFSET, "syntax-error", "error", str(exc))
        ]

    parents = _build_parent_map(tree)
    findings.extend(_check_functions(relative_file, tree))
    findings.extend(_check_classes(relative_file, tree))
    findings.extend(_check_magic_numbers(relative_file, tree, parents))
    findings.extend(_check_exception_handlers(relative_file, tree))
    return findings


def _check_functions(relative_file: str, tree: ast.AST) -> list[ReadabilityFinding]:
    """Check Python function definitions."""
    findings = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        findings.extend(_check_function_docstring(relative_file, node))
        findings.extend(_check_function_name(relative_file, node))
        findings.extend(_check_function_type_annotations(relative_file, node))
        findings.extend(_check_function_size(relative_file, node))
        findings.extend(_check_function_nesting(relative_file, node))
    return findings


def _check_classes(relative_file: str, tree: ast.AST) -> list[ReadabilityFinding]:
    """Check Python class definitions."""
    findings = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue
        docstring = ast.get_docstring(node) or ""
        if not docstring:
            findings.append(
                _finding(
                    relative_file,
                    node.lineno,
                    CLASS_DOCSTRING_RULE,
                    "error",
                    f"Class `{node.name}` must include a responsibility docstring.",
                )
            )
        findings.extend(_check_class_members(relative_file, node, docstring))
    return findings


def _check_magic_numbers(
    relative_file: str, tree: ast.AST, parents: dict[ast.AST, ast.AST]
) -> list[ReadabilityFinding]:
    """Check numeric literals outside named constants."""
    findings = []
    for node in ast.walk(tree):
        if not _is_numeric_constant(node):
            continue
        if _is_allowed_constant_number(node, parents):
            continue
        findings.append(
            _finding(
                relative_file,
                node.lineno,
                NO_MAGIC_NUMBER_RULE,
                "error",
                f"Numeric literal `{node.value}` must be moved into a named constant.",
            )
        )
    return findings


def _check_exception_handlers(
    relative_file: str, tree: ast.AST
) -> list[ReadabilityFinding]:
    """Check exception handlers for silent failure patterns."""
    findings = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ExceptHandler):
            continue
        if node.type is None or _handler_silently_passes(node):
            findings.append(
                _finding(
                    relative_file,
                    node.lineno,
                    NO_SILENT_EXCEPTION_RULE,
                    "error",
                    "Exception handlers must not silently swallow errors.",
                )
            )
    return findings


def _check_function_docstring(
    relative_file: str, node: ast.FunctionDef | ast.AsyncFunctionDef
) -> list[ReadabilityFinding]:
    """Check function docstring requirements."""
    docstring = ast.get_docstring(node) or ""
    if _is_test_function(node):
        return []
    if not docstring:
        return [
            _finding(
                relative_file,
                node.lineno,
                FUNCTION_DOCSTRING_RULE,
                "error",
                f"Function `{node.name}` must include a docstring.",
            )
        ]
    if _is_private_function(node):
        return []
    missing_sections = [
        section for section in DOCSTRING_REQUIRED_SECTIONS if section not in docstring
    ]
    if not missing_sections:
        return []
    return [
        _finding(
            relative_file,
            node.lineno,
            FUNCTION_DOCSTRING_RULE,
            "error",
            f"Function `{node.name}` must document Inputs, Outputs, and Side Effects.",
        )
    ]


def _check_function_name(
    relative_file: str, node: ast.FunctionDef | ast.AsyncFunctionDef
) -> list[ReadabilityFinding]:
    """Check whether a function name is semantic enough."""
    if _is_test_function(node) or _is_private_function(node):
        return []
    if node.name in GENERIC_FUNCTION_NAMES or len(node.name) <= len("run"):
        return [
            _finding(
                relative_file,
                node.lineno,
                SEMANTIC_FUNCTION_NAME_RULE,
                "warning",
                f"Function name `{node.name}` is too generic to explain intent.",
            )
        ]
    return []


def _check_function_type_annotations(
    relative_file: str, node: ast.FunctionDef | ast.AsyncFunctionDef
) -> list[ReadabilityFinding]:
    """Check public function parameter and return annotations."""
    if _is_test_function(node) or _is_private_function(node):
        return []
    missing = []
    for argument in node.args.args + node.args.kwonlyargs:
        if argument.arg in SELF_PARAMETER_NAMES:
            continue
        if argument.annotation is None:
            missing.append(argument.arg)
    if node.returns is None:
        missing.append("return")
    if not missing:
        return []
    return [
        _finding(
            relative_file,
            node.lineno,
            PUBLIC_FUNCTION_TYPE_ANNOTATIONS_RULE,
            "error",
            f"Function `{node.name}` is missing type annotations for: {', '.join(missing)}.",
        )
    ]


def _check_function_size(
    relative_file: str, node: ast.FunctionDef | ast.AsyncFunctionDef
) -> list[ReadabilityFinding]:
    """Check function line count threshold."""
    if node.end_lineno is None:
        return []
    line_count = node.end_lineno - node.lineno + LINE_COUNT_OFFSET
    if line_count <= MAX_FUNCTION_LINES:
        return []
    return [
        _finding(
            relative_file,
            node.lineno,
            FUNCTION_TOO_LONG_RULE,
            "warning",
            f"Function `{node.name}` has {line_count} lines and should be split.",
        )
    ]


def _check_function_nesting(
    relative_file: str, node: ast.FunctionDef | ast.AsyncFunctionDef
) -> list[ReadabilityFinding]:
    """Check nesting depth threshold."""
    nesting_depth = _max_nested_block_depth(node)
    if nesting_depth <= MAX_NESTING_DEPTH:
        return []
    return [
        _finding(
            relative_file,
            node.lineno,
            NESTING_TOO_DEEP_RULE,
            "warning",
            f"Function `{node.name}` has nesting depth {nesting_depth}.",
        )
    ]


def _check_class_members(
    relative_file: str, node: ast.ClassDef, docstring: str
) -> list[ReadabilityFinding]:
    """Check class member documentation."""
    findings = []
    for member in node.body:
        member_name = _class_member_name(member)
        if member_name is None or member_name.isupper():
            continue
        if member_name in docstring:
            continue
        findings.append(
            _finding(
                relative_file,
                member.lineno,
                CLASS_MEMBER_DOC_RULE,
                "error",
                f"Class member `{member_name}` must be documented.",
            )
        )
    return findings


def _check_semantic_file_name(
    relative_file: str, file_path: Path
) -> ReadabilityFinding | None:
    """Check whether a file name describes its module responsibility."""
    if file_path.stem in GENERIC_FILE_STEMS:
        return _finding(
            relative_file,
            LINE_COUNT_OFFSET,
            SEMANTIC_FILE_NAME_RULE,
            "warning",
            f"File name `{file_path.name}` is too generic to explain responsibility.",
        )
    return None


def _build_parent_map(tree: ast.AST) -> dict[ast.AST, ast.AST]:
    """Build a child-to-parent AST mapping."""
    parents = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            parents[child] = parent
    return parents


def _is_numeric_constant(node: ast.AST) -> bool:
    """Return whether a node is a numeric literal."""
    return (
        isinstance(node, ast.Constant)
        and isinstance(node.value, (int, float))
        and not isinstance(node.value, bool)
    )


def _is_allowed_constant_number(
    node: ast.AST, parents: dict[ast.AST, ast.AST]
) -> bool:
    """Return whether a numeric literal belongs to a named constant assignment."""
    current = node
    while current in parents:
        parent = parents[current]
        if isinstance(parent, ast.Assign):
            return all(_is_uppercase_name(target) for target in parent.targets)
        if isinstance(parent, ast.AnnAssign):
            return _is_uppercase_name(parent.target)
        if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return False
        current = parent
    return False


def _is_uppercase_name(node: ast.AST) -> bool:
    """Return whether an assignment target is an uppercase name."""
    return isinstance(node, ast.Name) and node.id.isupper()


def _handler_silently_passes(node: ast.ExceptHandler) -> bool:
    """Return whether an exception handler only passes."""
    return len(node.body) == LINE_COUNT_OFFSET and isinstance(
        node.body[FIRST_SEQUENCE_INDEX], ast.Pass
    )


def _is_test_function(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Return whether a function is a test function."""
    return node.name.startswith("test_")


def _is_private_function(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Return whether a function is private by naming convention."""
    return node.name.startswith("_")


def _class_member_name(node: ast.stmt) -> str | None:
    """Return class member name for simple class-level assignments."""
    if isinstance(node, ast.Assign) and len(node.targets) == LINE_COUNT_OFFSET:
        target = node.targets[FIRST_SEQUENCE_INDEX]
        if isinstance(target, ast.Name):
            return target.id
    if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
        return node.target.id
    return None


def _max_nested_block_depth(node: ast.AST) -> int:
    """Return maximum nested control-flow depth inside a node."""
    return max(
        (_nested_block_depth(child, ROOT_NESTING_DEPTH) for child in ast.iter_child_nodes(node)),
        default=INITIAL_NESTING_DEPTH,
    )


def _nested_block_depth(node: ast.AST, current_depth: int) -> int:
    """Return nested control-flow depth for a subtree."""
    next_depth = current_depth + LINE_COUNT_OFFSET if _is_nesting_node(node) else current_depth
    child_depth = [
        _nested_block_depth(child, next_depth) for child in ast.iter_child_nodes(node)
    ]
    return max([next_depth, *child_depth])


def _is_nesting_node(node: ast.AST) -> bool:
    """Return whether a node contributes to nesting depth."""
    return isinstance(
        node,
        (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith, ast.Try),
    )


def _finding(
    file: str, line: int, rule: str, severity: str, message: str
) -> ReadabilityFinding:
    """Create a readability finding."""
    return ReadabilityFinding(
        file=file,
        line=line,
        rule=rule,
        severity=severity,  # type: ignore[arg-type]
        message=message,
    )
