def test_can_import_cli_app() -> None:
    from pyignite.cli import app

    assert app.info.name == "pyignite"
