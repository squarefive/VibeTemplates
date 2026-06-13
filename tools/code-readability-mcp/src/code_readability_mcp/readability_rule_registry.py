"""Rule registry for code readability diagnostics."""

from __future__ import annotations

from .readability_result_models import RuleDescription


SUPPORTED_LANGUAGE = "python"
MAX_FUNCTION_LINES = 50
MAX_NESTING_DEPTH = 3

FUNCTION_DOCSTRING_RULE = "function-docstring"
CLASS_DOCSTRING_RULE = "class-docstring"
CLASS_MEMBER_DOC_RULE = "class-member-doc"
FILE_NOT_FOUND_RULE = "file-not-found"
NO_MAGIC_NUMBER_RULE = "no-magic-number"
SEMANTIC_FUNCTION_NAME_RULE = "semantic-function-name"
SEMANTIC_FILE_NAME_RULE = "semantic-file-name"
PUBLIC_FUNCTION_TYPE_ANNOTATIONS_RULE = "public-function-type-annotations"
NO_SILENT_EXCEPTION_RULE = "no-silent-exception"
FUNCTION_TOO_LONG_RULE = "function-too-long"
NESTING_TOO_DEEP_RULE = "nesting-too-deep"

READABILITY_RULES = [
    RuleDescription(
        FUNCTION_DOCSTRING_RULE,
        "error",
        "Public functions must document Inputs, Outputs, and Side Effects; private functions must include a docstring.",
    ),
    RuleDescription(
        CLASS_DOCSTRING_RULE,
        "error",
        "Classes must include a docstring explaining their responsibility.",
    ),
    RuleDescription(
        CLASS_MEMBER_DOC_RULE,
        "error",
        "Class member variables must be documented in the class docstring.",
    ),
    RuleDescription(
        FILE_NOT_FOUND_RULE,
        "error",
        "Explicitly requested files must exist and be readable.",
    ),
    RuleDescription(
        NO_MAGIC_NUMBER_RULE,
        "error",
        "Numeric literals are allowed only in named module-level or class-level constants.",
    ),
    RuleDescription(
        SEMANTIC_FUNCTION_NAME_RULE,
        "warning",
        "Function names must reveal intent and avoid vague names.",
    ),
    RuleDescription(
        SEMANTIC_FILE_NAME_RULE,
        "warning",
        "File names must describe module responsibility and avoid isolated generic names.",
    ),
    RuleDescription(
        PUBLIC_FUNCTION_TYPE_ANNOTATIONS_RULE,
        "error",
        "Public function parameters and return values must include type annotations.",
    ),
    RuleDescription(
        NO_SILENT_EXCEPTION_RULE,
        "error",
        "Exception handlers must not silently swallow errors.",
    ),
    RuleDescription(
        FUNCTION_TOO_LONG_RULE,
        "warning",
        f"Functions should not exceed {MAX_FUNCTION_LINES} lines.",
    ),
    RuleDescription(
        NESTING_TOO_DEEP_RULE,
        "warning",
        f"Nesting depth should not exceed {MAX_NESTING_DEPTH} blocks.",
    ),
]


def explain_rules_for_language(language: str) -> dict[str, object]:
    """Return active readability rules for one language.

    Inputs:
        language: Programming language identifier.

    Outputs:
        A dictionary containing language support status and rule descriptions.

    Side Effects:
        None.
    """
    if language != SUPPORTED_LANGUAGE:
        return {
            "language": language,
            "supported": False,
            "rules": [],
            "message": f"Unsupported language `{language}`. First version supports `python`.",
        }

    return {
        "language": language,
        "supported": True,
        "rules": [rule.to_dict() for rule in READABILITY_RULES],
    }
