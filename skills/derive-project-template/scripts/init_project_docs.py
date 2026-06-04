import argparse
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

TEMPLATE_INSTRUCTION_RE = re.compile(
    r"<!--\s*TEMPLATE-INSTRUCTION:.*?-->\s*", re.DOTALL
)
PLACEHOLDER_RE = re.compile(r"{{\s*([a-zA-Z0-9_]+)\s*}}")


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
    for key in REQUIRED_FIELDS:
        value = data[key]
        if value is None or value == "":
            value = "_Not provided._"
        if not isinstance(value, str):
            raise ValueError(f"Config field must be a string: {key}")
        normalized[key] = value
    return normalized


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
        "docs/ai-guidelines/AI-CODING-BEHAVIOR.md",
        "docs/ai-guidelines/COLLABORATION-PROTOCOL.md",
    ]
    for relative in guideline_targets:
        status = copy_file(TEMPLATE_ROOT / relative, output / relative, overwrite)
        results[status].append(relative)

    missing_fields = [
        key for key, value in sorted(config.items()) if value.strip() == "_Not provided._"
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
