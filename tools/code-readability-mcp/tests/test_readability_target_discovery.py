import subprocess

from code_readability_mcp.readability_target_discovery import (
    discover_all_python_files,
    discover_changed_python_files,
)


def test_discover_all_python_files_excludes_dependency_directories(tmp_path):
    source = tmp_path / "src"
    cache = tmp_path / "__pycache__"
    source.mkdir()
    cache.mkdir()
    (source / "reader.py").write_text("VALUE = 2\n", encoding="utf-8")
    (cache / "ignored.py").write_text("VALUE = 3\n", encoding="utf-8")

    files = discover_all_python_files(tmp_path)

    assert files == ["src/reader.py"]


def test_discover_changed_python_files_includes_untracked_files(tmp_path):
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    source = tmp_path / "reader.py"
    source.write_text("VALUE = 2\n", encoding="utf-8")

    files = discover_changed_python_files(tmp_path)

    assert files == ["reader.py"]
