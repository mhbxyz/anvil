from pathlib import Path

from flint.devloop import classify_changes


def test_classify_source_changes_restart_server(tmp_path: Path) -> None:
    decision = classify_changes(tmp_path, [str(tmp_path / "src" / "demo" / "main.py")])

    assert decision.restart_server is True
    assert decision.run_checks is True


def test_classify_test_changes_only_run_checks(tmp_path: Path) -> None:
    decision = classify_changes(tmp_path, [str(tmp_path / "tests" / "test_api.py")])

    assert decision.restart_server is False
    assert decision.run_checks is True
