from code_readability_mcp.python_readability_analyzer import analyze_python_readability
from code_readability_mcp.readability_rule_registry import (
    CLASS_MEMBER_DOC_RULE,
    FILE_NOT_FOUND_RULE,
    FUNCTION_DOCSTRING_RULE,
    NO_MAGIC_NUMBER_RULE,
)


def _write_python_file(root, relative_path, content):
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return relative_path


def _rule_ids(result):
    return {finding.rule for finding in result.findings}


def test_valid_public_function_passes(tmp_path):
    relative_path = _write_python_file(
        tmp_path,
        "src/pdf_section_parser.py",
        '''
MAX_RETRY_COUNT = 3

def parse_pdf_sections(path: str) -> list[str]:
    """Parse PDF sections from a local file.

    Inputs:
        path: Local PDF file path.

    Outputs:
        Parsed section titles.

    Side Effects:
        None.
    """
    return [path]
''',
    )

    result = analyze_python_readability(str(tmp_path), [relative_path])

    assert result.findings == []


def test_missing_docstring_sections_are_reported(tmp_path):
    relative_path = _write_python_file(
        tmp_path,
        "src/pdf_section_parser.py",
        '''
def parse_pdf_sections(path: str) -> list[str]:
    """Parse PDF sections."""
    return [path]
''',
    )

    result = analyze_python_readability(str(tmp_path), [relative_path])

    assert FUNCTION_DOCSTRING_RULE in _rule_ids(result)


def test_magic_number_in_logic_is_reported(tmp_path):
    relative_path = _write_python_file(
        tmp_path,
        "src/pdf_section_parser.py",
        '''
def parse_pdf_sections(path: str) -> list[str]:
    """Parse PDF sections.

    Inputs:
        path: Local PDF file path.

    Outputs:
        Parsed section titles.

    Side Effects:
        None.
    """
    return [path] * 3
''',
    )

    result = analyze_python_readability(str(tmp_path), [relative_path])

    assert NO_MAGIC_NUMBER_RULE in _rule_ids(result)


def test_annotated_class_member_requires_documentation(tmp_path):
    relative_path = _write_python_file(
        tmp_path,
        "src/paper_reader.py",
        '''
class PaperReader:
    """Read papers."""

    timeout_seconds: int
''',
    )

    result = analyze_python_readability(str(tmp_path), [relative_path])

    assert CLASS_MEMBER_DOC_RULE in _rule_ids(result)


def test_missing_file_returns_structured_finding(tmp_path):
    result = analyze_python_readability(str(tmp_path), ["src/missing.py"])

    assert len(result.findings) == 1
    finding = result.findings[0]
    assert finding.rule == FILE_NOT_FOUND_RULE
    assert finding.severity == "error"
    assert finding.file == "src/missing.py"
