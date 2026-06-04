import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "derive-project-template"
INIT_SCRIPT = SKILL / "scripts" / "init_project_docs.py"
VALIDATE_SCRIPT = SKILL / "scripts" / "validate_project_docs.py"


def run_script(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def write_config(path: Path, **overrides: str) -> None:
    data = {
        "project_name": "SampleProject",
        "project_context": "_Not provided._",
        "overview": "_Not provided._",
        "features_section": "_Not provided._",
        "project_structure": "_Not provided._",
        "getting_started": "_Not provided._",
        "development": "_Not provided._",
        "functional_scope_section": "_Not provided._",
        "module_map_section": "_Not provided._",
        "project_specific_agent_rules": "_Not provided._",
    }
    data.update(overrides)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def test_generates_docs_without_template_artifacts(tmp_path: Path) -> None:
    config = tmp_path / "project.json"
    output = tmp_path / "out"
    write_config(
        config,
        project_context="A template-derived documentation project.",
        functional_scope_section=(
            "| Feature | Status | Notes |\n"
            "| --- | --- | --- |\n"
            "| Generate project docs | implemented | Creates the core document set. |"
        ),
        module_map_section=(
            "| Module | Responsibility | Main Files | Notes |\n"
            "| --- | --- | --- | --- |\n"
            "| Generator | Renders templates. | `scripts/init_project_docs.py` | Does not overwrite by default. |"
        ),
    )

    result = run_script(INIT_SCRIPT, "--config", str(config), "--output", str(output))

    assert result.returncode == 0, result.stderr
    agents = (output / "AGENTS.md").read_text(encoding="utf-8")
    readme = (output / "README.md").read_text(encoding="utf-8")
    assert "TEMPLATE-INSTRUCTION" not in agents + readme
    assert "{{" not in agents + readme
    assert "## Guideline Index" in agents
    assert "docs/ai-guidelines/AI-CODING-BEHAVIOR.md" in agents
    assert "docs/ai-guidelines/COLLABORATION-PROTOCOL.md" in agents
    assert "## Functional Scope And Completeness" in agents
    assert "A template-derived documentation project." in agents
    assert (output / "docs" / "ai-guidelines" / "AI-CODING-BEHAVIOR.md").exists()
    assert (
        output / "docs" / "ai-guidelines" / "COLLABORATION-PROTOCOL.md"
    ).exists()


def test_generation_does_not_overwrite_existing_files(tmp_path: Path) -> None:
    config = tmp_path / "project.json"
    output = tmp_path / "out"
    output.mkdir()
    existing = output / "README.md"
    existing.write_text("keep me", encoding="utf-8")
    write_config(config)

    result = run_script(INIT_SCRIPT, "--config", str(config), "--output", str(output))

    assert result.returncode == 0, result.stderr
    assert existing.read_text(encoding="utf-8") == "keep me"
    assert "skipped" in result.stdout.lower()


def test_validator_accepts_generated_structure(tmp_path: Path) -> None:
    config = tmp_path / "project.json"
    output = tmp_path / "out"
    write_config(config)
    generated = run_script(INIT_SCRIPT, "--config", str(config), "--output", str(output))
    assert generated.returncode == 0, generated.stderr

    result = run_script(VALIDATE_SCRIPT, "--path", str(output))

    assert result.returncode == 0, result.stdout + result.stderr
    assert "validation passed" in result.stdout.lower()


def test_validator_rejects_missing_required_section(tmp_path: Path) -> None:
    output = tmp_path / "out"
    output.mkdir()
    (output / "AGENTS.md").write_text("# AGENTS.md\n\n## Project Context\n", encoding="utf-8")
    (output / "README.md").write_text(
        "# SampleProject\n\n## Overview\n\n## Features\n\n## Project Structure\n\n## Getting Started\n\n## Development\n",
        encoding="utf-8",
    )
    guideline_dir = output / "docs" / "ai-guidelines"
    guideline_dir.mkdir(parents=True)
    (guideline_dir / "AI-CODING-BEHAVIOR.md").write_text(
        "AI guidance", encoding="utf-8"
    )
    (guideline_dir / "COLLABORATION-PROTOCOL.md").write_text(
        "Collaboration guidance", encoding="utf-8"
    )

    result = run_script(VALIDATE_SCRIPT, "--path", str(output))

    assert result.returncode != 0
    assert "Functional Scope And Completeness" in result.stdout
