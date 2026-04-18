"""Main TUI application."""

from pathlib import Path

from textual.app import App

from cookie_taster.tui.screens.execution import ExecutionScreen
from cookie_taster.tui.screens.options import OptionsScreen
from cookie_taster.tui.screens.template import TemplateScreen


class CookieTasterApp(App[None]):
    """Cookie Taster TUI application."""

    TITLE = "Cookie Taster"
    CSS = """
    Screen {
        background: $surface;
    }
    """

    def __init__(
        self,
        output_dir: Path,
        template_source: str = "",
    ) -> None:
        """
        Initialize the application.

        Args:
            output_dir: Directory where projects will be generated.
            template_source: Optional pre-filled template source.

        """
        super().__init__()
        self.output_dir = output_dir
        self.template_source = template_source

    def on_mount(self) -> None:
        """Handle app mount."""
        self._show_template_screen()

    def _show_template_screen(self) -> None:
        """Show the template input screen."""
        screen = TemplateScreen(self.template_source)
        self.push_screen(screen, self._handle_template_result)

    def _handle_template_result(self, result: tuple[str, list, dict] | None) -> None:  # type: ignore[type-arg]
        """
        Handle result from template screen.

        Args:
            result: Tuple of (template_source, options, context) or None if cancelled.

        """
        if result is None:
            self.exit()
            return

        template_source, options, context = result
        self.template_source = template_source

        # Show options selection screen
        screen = OptionsScreen(options)
        self.push_screen(
            screen,
            lambda selections: self._handle_options_result(
                selections, template_source, options, context
            ),
        )

    def _handle_options_result(
        self,
        selections: dict[str, list[str]] | None,
        template_source: str,
        options: list,  # type: ignore[type-arg]
        context: dict,  # type: ignore[type-arg]
    ) -> None:
        """
        Handle result from options screen.

        Args:
            selections: Selected values for each option, or None if cancelled.
            template_source: The template source.
            options: List of template options.
            context: The full template context.

        """
        if selections is None:
            # User went back, return to template screen
            return

        # Show execution screen
        screen = ExecutionScreen(
            template_source=template_source,
            options=options,
            selections=selections,
            output_dir=self.output_dir,
            base_context=context,
        )
        self.push_screen(screen)


def run_tui(output_dir: Path, template_source: str = "") -> None:
    """
    Run the TUI application.

    Args:
        output_dir: Directory where projects will be generated.
        template_source: Optional pre-filled template source.

    """
    app = CookieTasterApp(output_dir=output_dir, template_source=template_source)
    app.run()
