import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "derive-project-template"
INIT_SCRIPT = SKILL / "scripts" / "init_project_docs.py"
VALIDATE_SCRIPT = SKILL / "scripts" / "validate_project_docs.py"
AUDIT_SCRIPT = SKILL / "scripts" / "audit_project_docs.py"
REPO_KARPATHY_SKILL = ROOT / ".agents" / "skills" / "karpathy-guidelines" / "SKILL.md"
TEMPLATE_KARPATHY_SKILL = (
    SKILL
    / "assets"
    / "templates"
    / ".agents"
    / "skills"
    / "karpathy-guidelines"
    / "SKILL.md"
)
BUNDLED_VSCODE_TRANSLATION_VSIX = (
    SKILL
    / "assets"
    / "tools"
    / "vscode"
    / "markdown-chinese-preview-translator-0.0.1.vsix"
)


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
    codebase_map = (output / "docs" / "architecture" / "codebase-map.md").read_text(
        encoding="utf-8"
    )
    design_principles = (
        output / "docs" / "engineering-guidelines" / "DESIGN-PRINCIPLES.md"
    ).read_text(encoding="utf-8")
    assert "TEMPLATE-INSTRUCTION" not in agents + readme + codebase_map + design_principles
    assert "{{" not in agents + readme + codebase_map + design_principles
    assert "## AGENTS.md Role" in agents
    assert "## Context Loading Rules" in agents
    assert "AI coding work entry point" in agents
    assert "top-level index" in agents
    assert "Does not replace" in agents
    assert "AI-CODING-BEHAVIOR.md" not in agents
    assert "docs/ai-guidelines/COLLABORATION-PROTOCOL.md" in agents
    assert "docs/engineering-guidelines/DESIGN-PRINCIPLES.md" in agents
    assert "docs/architecture/codebase-map.md" in agents
    assert "## Functional Scope And Completeness" in agents
    assert "A template-derived documentation project." in agents
    assert "## 目录说明" in codebase_map
    assert "## 文件说明" in codebase_map
    assert "## Layering Guidance" in design_principles
    assert (output / "scripts" / "check-codebase-map-format.py").exists()
    assert not (output / "docs" / "ai-guidelines" / "AI-CODING-BEHAVIOR.md").exists()
    assert (
        output / "docs" / "ai-guidelines" / "COLLABORATION-PROTOCOL.md"
    ).exists()
    collaboration_protocol = (
        output / "docs" / "ai-guidelines" / "COLLABORATION-PROTOCOL.md"
    ).read_text(encoding="utf-8")
    assert "### 1.4 Document Change Details" in collaboration_protocol
    assert "Document Change Details:" in collaboration_protocol
    assert "### 1.5 Branch Strategy" in collaboration_protocol
    assert "### 1.6 Merge Strategy" in collaboration_protocol
    assert (
        output / ".agents" / "skills" / "karpathy-guidelines" / "SKILL.md"
    ).exists()
    assert not (output / "docs" / "agents").exists()
    assert not (output / "scripts" / "check-agent-doc-format.py").exists()


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


def test_audit_accepts_generated_structure(tmp_path: Path) -> None:
    config = tmp_path / "project.json"
    output = tmp_path / "out"
    write_config(config)
    generated = run_script(INIT_SCRIPT, "--config", str(config), "--output", str(output))
    assert generated.returncode == 0, generated.stderr

    result = run_script(AUDIT_SCRIPT, "--path", str(output))

    assert result.returncode == 0, result.stdout + result.stderr
    assert "- status: ok" in result.stdout
    assert "Incremental Update Scope" in result.stdout
    assert "Replace" not in result.stdout


def test_audit_reports_missing_design_principles_incrementally(tmp_path: Path) -> None:
    config = tmp_path / "project.json"
    output = tmp_path / "out"
    write_config(config)
    generated = run_script(INIT_SCRIPT, "--config", str(config), "--output", str(output))
    assert generated.returncode == 0, generated.stderr
    (output / "docs" / "engineering-guidelines" / "DESIGN-PRINCIPLES.md").unlink()

    result = run_script(AUDIT_SCRIPT, "--path", str(output))

    assert result.returncode == 1
    assert "Missing:" in result.stdout
    assert "docs/engineering-guidelines/DESIGN-PRINCIPLES.md" in result.stdout
    assert "Add:" in result.stdout
    assert "Replace" not in result.stdout


def test_audit_reports_outdated_agents_structure_incrementally(tmp_path: Path) -> None:
    config = tmp_path / "project.json"
    output = tmp_path / "out"
    write_config(config)
    generated = run_script(INIT_SCRIPT, "--config", str(config), "--output", str(output))
    assert generated.returncode == 0, generated.stderr
    agents = output / "AGENTS.md"
    agents.write_text(
        agents.read_text(encoding="utf-8").replace("## Context Loading Rules", "## Old Rules"),
        encoding="utf-8",
    )

    result = run_script(AUDIT_SCRIPT, "--path", str(output))

    assert result.returncode == 1
    assert "Structure Mismatches:" in result.stdout
    assert "Missing section: `## Context Loading Rules`" in result.stdout
    assert "Modify:" in result.stdout
    assert "preserving existing project context" in result.stdout
    assert "Replace" not in result.stdout


def test_audit_reports_invalid_codebase_map(tmp_path: Path) -> None:
    config = tmp_path / "project.json"
    output = tmp_path / "out"
    write_config(config)
    generated = run_script(INIT_SCRIPT, "--config", str(config), "--output", str(output))
    assert generated.returncode == 0, generated.stderr
    (output / "docs" / "architecture" / "codebase-map.md").write_text(
        "# SampleProject 代码地图\n", encoding="utf-8"
    )

    result = run_script(AUDIT_SCRIPT, "--path", str(output))

    assert result.returncode == 1
    assert "Invalid:" in result.stdout
    assert "Codebase map checker failed" in result.stdout
    assert "Modify:" in result.stdout
    assert "Replace" not in result.stdout


def test_audit_does_not_check_python_checker_placeholders(tmp_path: Path) -> None:
    config = tmp_path / "project.json"
    output = tmp_path / "out"
    write_config(config)
    generated = run_script(INIT_SCRIPT, "--config", str(config), "--output", str(output))
    assert generated.returncode == 0, generated.stderr
    checker = output / "scripts" / "check-codebase-map-format.py"
    checker.write_text(
        checker.read_text(encoding="utf-8")
        + '\nPLACEHOLDER_RE_FOR_TEST = r"\\{\\{[^}]+\\}\\}"\n',
        encoding="utf-8",
    )

    result = run_script(AUDIT_SCRIPT, "--path", str(output))

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Contains unresolved template placeholder" not in result.stdout


def test_audit_reports_failed_for_missing_path(tmp_path: Path) -> None:
    missing = tmp_path / "missing"

    result = run_script(AUDIT_SCRIPT, "--path", str(missing))

    assert result.returncode == 2
    assert "- status: failed" in result.stdout
    assert "Audit target path does not exist or is not a directory" in result.stdout
    assert "Replace" not in result.stdout


def test_bundled_karpathy_guidelines_matches_repo_skill() -> None:
    assert TEMPLATE_KARPATHY_SKILL.read_text(
        encoding="utf-8"
    ) == REPO_KARPATHY_SKILL.read_text(encoding="utf-8")


def test_bundled_vscode_translation_vsix_exists() -> None:
    assert BUNDLED_VSCODE_TRANSLATION_VSIX.exists()
    assert BUNDLED_VSCODE_TRANSLATION_VSIX.stat().st_size > 0


def test_skill_mentions_code_readability_mcp_configuration() -> None:
    skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    assert "tools/code-readability-mcp" in skill
    assert "ask before" in skill
    assert "local Codex MCP configuration" in skill


def test_generates_agent_context_when_agent_fields_are_provided(tmp_path: Path) -> None:
    config = tmp_path / "project.json"
    output = tmp_path / "out"
    write_config(
        config,
        agent_module_name="personal_knowledge_agent",
        agent_chinese_name="个人知识",
        agent_language="Python",
        agent_type="Tool-Using Agent",
        agent_background="Handles personal knowledge retrieval for saved notes.",
        agent_core_goals="1. Retrieve relevant notes.\n2. Summarize grounded answers.",
        agent_tool_table_rows=(
            "| search_notes | Retrieve notes. | User asks a knowledge question. | No | No |"
        ),
        agent_tool_contract_name="search_notes",
        agent_tool_input_json_fields='"query": "string"',
        agent_acceptance_checklist="1. Answers cite retrieved sources.",
    )

    generated = run_script(INIT_SCRIPT, "--config", str(config), "--output", str(output))

    assert generated.returncode == 0, generated.stderr
    agent_doc = output / "docs" / "agents" / "personal_knowledge_agent.md"
    checker = output / "scripts" / "check-agent-doc-format.py"
    assert agent_doc.exists()
    assert checker.exists()
    assert not (output / "docs" / "templates" / "agent-development-context.template.md").exists()

    agents = (output / "AGENTS.md").read_text(encoding="utf-8")
    agent_content = agent_doc.read_text(encoding="utf-8")
    assert "## Agent Development Context Index" in agents
    assert "docs/agents/personal_knowledge_agent.md" in agents
    assert "# 个人知识 Agent 开发上下文" in agent_content
    assert "Handles personal knowledge retrieval for saved notes." in agent_content
    assert "search_notes" in agent_content
    assert '"query": "string"' in agent_content
    assert "Answers cite retrieved sources." in agent_content
    assert "不得记录单次任务计划" in agent_content
    assert "临时实施步骤" in agent_content
    assert "Git 分支安排" in agent_content
    assert "工作进度" in agent_content
    assert "当前对话待办" in agent_content
    assert "Agent Runtime / Loop 职责" in agent_content
    assert "TEMPLATE-INSTRUCTION" not in agent_content
    assert "{{" not in agent_content

    validation = run_script(VALIDATE_SCRIPT, "--path", str(output))

    assert validation.returncode == 0, validation.stdout + validation.stderr
    assert "validation passed" in validation.stdout.lower()

    checker_result = subprocess.run(
        [sys.executable, str(checker), "docs/agents/personal_knowledge_agent.md"],
        cwd=output,
        text=True,
        capture_output=True,
    )
    assert checker_result.returncode == 0, checker_result.stdout + checker_result.stderr


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
    (guideline_dir / "COLLABORATION-PROTOCOL.md").write_text(
        "Collaboration guidance", encoding="utf-8"
    )
    design_principles = (
        output / "docs" / "engineering-guidelines" / "DESIGN-PRINCIPLES.md"
    )
    design_principles.parent.mkdir(parents=True)
    design_principles.write_text("Design guidance", encoding="utf-8")
    codebase_map = output / "docs" / "architecture" / "codebase-map.md"
    codebase_map.parent.mkdir(parents=True)
    codebase_map.write_text(
        "---\n"
        "title: \"SampleProject 代码地图\"\n"
        "last_updated: \"2026-06-19\"\n"
        "---\n\n"
        "# SampleProject 代码地图\n\n"
        "## 目录说明\n\n"
        "| 目录 | 作用 |\n"
        "|---|---|\n"
        "| `_Not provided._` | _Not provided._ |\n\n"
        "## 文件说明\n\n"
        "### _Not provided._\n\n"
        "模块目录：`_Not provided._`\n\n"
        "模块作用：_Not provided._\n\n"
        "| 文件 | 作用 |\n"
        "|---|---|\n"
        "| `_Not provided._` | _Not provided._ |\n",
        encoding="utf-8",
    )
    codebase_checker = output / "scripts" / "check-codebase-map-format.py"
    codebase_checker.parent.mkdir(parents=True)
    codebase_checker.write_text(
        (SKILL / "assets" / "templates" / "scripts" / "check-codebase-map-format.py").read_text(
            encoding="utf-8"
        ),
        encoding="utf-8",
    )
    karpathy_skill = output / ".agents" / "skills" / "karpathy-guidelines" / "SKILL.md"
    karpathy_skill.parent.mkdir(parents=True)
    karpathy_skill.write_text("Karpathy guidance", encoding="utf-8")

    result = run_script(VALIDATE_SCRIPT, "--path", str(output))

    assert result.returncode != 0
    assert "Functional Scope And Completeness" in result.stdout


def test_validator_rejects_invalid_codebase_map(tmp_path: Path) -> None:
    config = tmp_path / "project.json"
    output = tmp_path / "out"
    write_config(config)
    generated = run_script(INIT_SCRIPT, "--config", str(config), "--output", str(output))
    assert generated.returncode == 0, generated.stderr

    codebase_map = output / "docs" / "architecture" / "codebase-map.md"
    codebase_map.write_text("# SampleProject 代码地图\n", encoding="utf-8")

    result = run_script(VALIDATE_SCRIPT, "--path", str(output))

    assert result.returncode != 0
    assert "Codebase map format check failed" in result.stdout
    assert "missing YAML frontmatter" in result.stdout
