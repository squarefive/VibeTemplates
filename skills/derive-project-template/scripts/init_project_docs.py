import argparse
import datetime as dt
import json
import re
import shutil
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "templates"

REQUIRED_FIELDS = {
    "project_name",
    "project_context",
    "overview",
    "features_section",
    "project_structure",
    "getting_started",
    "development",
    "functional_scope_section",
    "module_map_section",
    "project_specific_agent_rules",
}

OPTIONAL_AGENT_FIELDS = {
    "agent_module_name",
    "agent_chinese_name",
    "agent_language",
    "agent_type",
    "agent_background",
    "agent_core_value",
    "agent_role",
    "agent_core_goals",
    "agent_included_capabilities",
    "agent_excluded_capabilities",
    "agent_behavior_constraints",
    "agent_loop_responsibilities",
    "agent_prompt_builder_responsibilities",
    "agent_tools_responsibilities",
    "agent_services_repositories_responsibilities",
    "agent_storage_external_api_responsibilities",
    "agent_core_files_table_rows",
    "agent_tool_table_rows",
    "agent_tool_contract_name",
    "agent_tool_contract_responsibility",
    "agent_tool_input_json_fields",
    "agent_tool_output_json_fields",
    "agent_tool_side_effects",
    "agent_tool_failure_handling",
    "agent_runtime_context_sources",
    "agent_long_term_memory_sources",
    "agent_memory_exclusions",
    "agent_context_trimming_rules",
    "agent_core_workflow_name",
    "agent_core_workflow_steps",
    "agent_core_workflow_success_conditions",
    "agent_core_workflow_failure_conditions",
    "agent_core_workflow_user_feedback",
    "agent_data_model_name",
    "agent_data_model_table_rows",
    "agent_data_constraints",
    "agent_failure_mode_table_rows",
    "agent_degradation_principles",
    "agent_unit_tests",
    "agent_integration_tests",
    "agent_regression_tests",
    "agent_acceptance_checklist",
    "agent_initial_commit",
}

OPTIONAL_AGENT_FIELD_DEFAULTS = {
    "agent_core_goals": "1. _Not provided._",
    "agent_included_capabilities": "1. _Not provided._",
    "agent_excluded_capabilities": "1. _Not provided._",
    "agent_behavior_constraints": "1. _Not provided._",
    "agent_loop_responsibilities": "- _Not provided._",
    "agent_prompt_builder_responsibilities": "- _Not provided._",
    "agent_tools_responsibilities": "- _Not provided._",
    "agent_services_repositories_responsibilities": "- _Not provided._",
    "agent_storage_external_api_responsibilities": "- _Not provided._",
    "agent_core_files_table_rows": "| _Not provided._ | _Not provided._ |",
    "agent_tool_table_rows": (
        "| _Not provided._ | _Not provided._ | _Not provided._ | "
        "_Not provided._ | _Not provided._ |"
    ),
    "agent_tool_contract_name": "_Not provided._",
    "agent_tool_input_json_fields": '"not_provided": "_Not provided._"',
    "agent_tool_output_json_fields": '"not_provided": "_Not provided._"',
    "agent_runtime_context_sources": "1. _Not provided._",
    "agent_long_term_memory_sources": "1. _Not provided._",
    "agent_memory_exclusions": "1. _Not provided._",
    "agent_context_trimming_rules": "1. _Not provided._",
    "agent_core_workflow_name": "_Not provided._",
    "agent_core_workflow_steps": "1. _Not provided._",
    "agent_data_model_name": "_Not provided._",
    "agent_data_model_table_rows": (
        "| _Not provided._ | _Not provided._ | _Not provided._ | _Not provided._ |"
    ),
    "agent_data_constraints": "1. _Not provided._",
    "agent_failure_mode_table_rows": (
        "| _Not provided._ | _Not provided._ | _Not provided._ | _Not provided._ |"
    ),
    "agent_degradation_principles": "1. _Not provided._",
    "agent_unit_tests": "1. _Not provided._",
    "agent_integration_tests": "1. _Not provided._",
    "agent_regression_tests": "1. _Not provided._",
    "agent_acceptance_checklist": "1. _Not provided._",
}

TEMPLATE_INSTRUCTION_RE = re.compile(
    r"<!--\s*TEMPLATE-INSTRUCTION:.*?-->\s*", re.DOTALL
)
PLACEHOLDER_RE = re.compile(r"{{\s*([a-zA-Z0-9_]+)\s*}}")
SAFE_AGENT_FILENAME_RE = re.compile(r"[^a-zA-Z0-9_.-]+")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate minimal project docs from derive-project-template templates."
    )
    parser.add_argument("--config", required=True, help="Path to JSON config file.")
    parser.add_argument("--output", required=True, help="Target project directory.")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing generated files. Defaults to skip.",
    )
    return parser.parse_args()


def load_config(config_path: Path) -> dict[str, str]:
    with config_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    missing = sorted(REQUIRED_FIELDS - set(data))
    if missing:
        raise ValueError(f"Missing required config fields: {', '.join(missing)}")

    normalized = {}
    for key in REQUIRED_FIELDS | OPTIONAL_AGENT_FIELDS:
        default = OPTIONAL_AGENT_FIELD_DEFAULTS.get(key, "_Not provided._")
        value = data.get(key, default)
        if value is None or value == "":
            value = default
        if not isinstance(value, str):
            raise ValueError(f"Config field must be a string: {key}")
        normalized[key] = value
    return normalized


def has_value(value: str) -> bool:
    return value.strip() != "_Not provided._"


def safe_agent_filename(module_name: str) -> str:
    safe_name = SAFE_AGENT_FILENAME_RE.sub("-", module_name.strip()).strip(".-")
    if not safe_name:
        raise ValueError("agent_module_name does not produce a valid filename")
    return safe_name


def agent_project_enabled(config: dict[str, str]) -> bool:
    return has_value(config["agent_module_name"]) and has_value(
        config["agent_chinese_name"]
    )


def with_agent_context(config: dict[str, str]) -> dict[str, str]:
    extended = dict(config)
    extended["agent_development_context_index"] = ""
    extended["last_updated"] = dt.date.today().isoformat()

    if agent_project_enabled(extended):
        agent_file = f"docs/agents/{safe_agent_filename(extended['agent_module_name'])}.md"
        extended["agent_doc_path"] = agent_file
        extended[
            "agent_development_context_index"
        ] = (
            "## Agent Development Context Index\n"
            f"- `{agent_file}`: Agent development context defining role boundaries, "
            "tool contracts, data boundaries, workflows, failure modes, and testing "
            "requirements.\n"
        )
    else:
        extended["agent_doc_path"] = ""
    return extended


def render_template(template: str, config: dict[str, str]) -> str:
    without_instructions = TEMPLATE_INSTRUCTION_RE.sub("", template)

    def replace(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in config:
            raise ValueError(f"Template references unknown placeholder: {key}")
        return config[key]

    rendered = PLACEHOLDER_RE.sub(replace, without_instructions)
    return rendered.rstrip() + "\n"


def write_file(path: Path, content: str, overwrite: bool) -> str:
    if path.exists() and not overwrite:
        return "skipped"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return "generated"


def copy_file(source: Path, destination: Path, overwrite: bool) -> str:
    if destination.exists() and not overwrite:
        return "skipped"
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    return "generated"


def generate(config: dict[str, str], output: Path, overwrite: bool) -> dict[str, list[str]]:
    results: dict[str, list[str]] = {"generated": [], "skipped": []}
    config = with_agent_context(config)

    template_targets = {
        "AGENTS.md.tpl": "AGENTS.md",
        "README.md.tpl": "README.md",
    }
    for template_name, target_name in template_targets.items():
        template = (TEMPLATE_ROOT / template_name).read_text(encoding="utf-8")
        content = render_template(template, config)
        status = write_file(output / target_name, content, overwrite)
        results[status].append(target_name)

    guideline_targets = [
        "docs/ai-guidelines/COLLABORATION-PROTOCOL.md",
    ]
    for relative in guideline_targets:
        status = copy_file(TEMPLATE_ROOT / relative, output / relative, overwrite)
        results[status].append(relative)

    karpathy_skill = ".agents/skills/karpathy-guidelines/SKILL.md"
    status = copy_file(TEMPLATE_ROOT / karpathy_skill, output / karpathy_skill, overwrite)
    results[status].append(karpathy_skill)

    if agent_project_enabled(config):
        agent_template = (
            TEMPLATE_ROOT / "docs" / "agents" / "agent-development-context.md.tpl"
        ).read_text(encoding="utf-8")
        agent_content = render_template(agent_template, config)
        status = write_file(output / config["agent_doc_path"], agent_content, overwrite)
        results[status].append(config["agent_doc_path"])

        checker = "scripts/check-agent-doc-format.py"
        status = copy_file(TEMPLATE_ROOT / checker, output / checker, overwrite)
        results[status].append(checker)

    missing_fields = [
        key
        for key in sorted(REQUIRED_FIELDS)
        if config[key].strip() == "_Not provided._"
    ]
    if missing_fields:
        results["missing-but-rendered"] = missing_fields

    return results


def main() -> int:
    args = parse_args()
    try:
        config = load_config(Path(args.config))
        results = generate(config, Path(args.output), args.overwrite)
    except Exception as exc:
        print(f"error: {exc}")
        return 1

    for key in ("generated", "skipped", "missing-but-rendered"):
        values = results.get(key, [])
        if values:
            print(f"{key}:")
            for value in values:
                print(f"  - {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
