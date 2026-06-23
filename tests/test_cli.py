from typer.testing import CliRunner

from cookie_taster.cli import app

runner = CliRunner()


def test_help():
    """The help message includes the CLI description."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "cookiecutter template" in result.stdout
