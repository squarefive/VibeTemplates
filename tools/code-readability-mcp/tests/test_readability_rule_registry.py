from code_readability_mcp.readability_rule_registry import (
    FUNCTION_DOCSTRING_RULE,
    SUPPORTED_LANGUAGE,
    explain_rules_for_language,
)


def test_explain_rules_for_python_includes_docstring_rule():
    result = explain_rules_for_language(SUPPORTED_LANGUAGE)

    assert result["supported"] is True
    rule_ids = {rule["id"] for rule in result["rules"]}
    assert FUNCTION_DOCSTRING_RULE in rule_ids


def test_explain_rules_for_unsupported_language_returns_clear_message():
    result = explain_rules_for_language("typescript")

    assert result["supported"] is False
    assert result["rules"] == []
    assert "Unsupported language" in result["message"]
