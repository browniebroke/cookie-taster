"""Command-line interface for Cookie Taster."""

from pathlib import Path
from typing import Annotated

import typer
from rich import print

from cookie_taster.tui.app import run_tui

app = typer.Typer(
    help="Cookie Taster - Test cookiecutter templates with multiple option combinations"
)


@app.command()
def test(
    template: Annotated[
        str | None,
        typer.Argument(
            help=(
                "Template source (URL, path, etc.). "
                "If not provided, you'll be prompted."
            )
        ),
    ] = None,
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            "-o",
            help="Directory where generated projects will be saved",
        ),
    ] = Path("./cookie-taster-output"),
) -> None:
    """
    Launch the TUI to test a cookiecutter template.

    This command starts an interactive TUI that allows you to:
    1. Specify a cookiecutter template
    2. Select multiple values for template options
    3. Generate all combinations of projects
    4. Run tasters to validate each generated project

    Examples:
        # Launch TUI and provide template interactively
        cookie-taster test

        # Pre-fill the template source
        cookie-taster test https://github.com/cookiecutter/cookiecutter-django

        # Specify custom output directory
        cookie-taster test -o ./my-test-projects

    """
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[cyan]Output directory:[/cyan] {output_dir.resolve()}")

    # Launch the TUI
    run_tui(output_dir=output_dir, template_source=template or "")
