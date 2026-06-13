from pathlib import Path

from code_readability_mcp.python_readability_analyzer import analyze_python_readability


def test_code_readability_mcp_source_has_no_error_findings():
    root = Path(__file__).resolve().parents[1]
    source_root = root / "src" / "code_readability_mcp"
    files = [path.relative_to(root).as_posix() for path in sorted(source_root.glob("*.py"))]

    result = analyze_python_readability(str(root), files)

    error_findings = [
        finding.to_dict() for finding in result.findings if finding.severity == "error"
    ]
    assert error_findings == []
