def test_can_import_cli_app() -> None:
    from pyqck.cli import app

    assert app.info.name == "pyqck"
