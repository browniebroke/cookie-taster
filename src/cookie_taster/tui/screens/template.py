"""Template input screen."""

from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Static

from cookie_taster.core.template import TemplateInspector, TemplateOption


class TemplateScreen(Screen[tuple[str, list[TemplateOption], dict[str, object]]]):
    """Screen for inputting the template source."""

    CSS = """
    TemplateScreen {
        align: center middle;
    }

    #template-container {
        width: 80;
        height: auto;
        border: solid $primary;
        padding: 1 2;
    }

    #title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }

    #description {
        text-align: center;
        color: $text-muted;
        margin-bottom: 2;
    }

    #error {
        color: $error;
        text-align: center;
        margin-top: 1;
        height: 1;
    }

    Input {
        margin-bottom: 1;
    }

    #buttons {
        align: center middle;
        margin-top: 1;
    }

    Button {
        margin: 0 1;
    }
    """

    def __init__(self, template_source: str = "") -> None:
        """
        Initialize the template screen.

        Args:
            template_source: Optional pre-filled template source.

        """
        super().__init__()
        self.template_source = template_source

    def compose(self) -> ComposeResult:
        """Compose the UI."""
        yield Header()
        with Center():
            with Vertical(id="template-container"):
                yield Static("Cookie Taster", id="title")
                yield Static(
                    "Enter a cookiecutter template source (URL, path, etc.)",
                    id="description",
                )
                yield Input(
                    placeholder="https://github.com/user/template or /path/to/template",
                    value=self.template_source,
                    id="template-input",
                )
                yield Static("", id="error")
                with Center(id="buttons"):
                    yield Button("Continue", variant="primary", id="continue-btn")
                    yield Button("Quit", variant="default", id="quit-btn")
        yield Footer()

    @on(Button.Pressed, "#continue-btn")
    async def handle_continue(self) -> None:
        """Handle continue button press."""
        input_widget = self.query_one("#template-input", Input)
        template_source = input_widget.value.strip()

        if not template_source:
            self._show_error("Please enter a template source")
            return

        # Show loading state
        self._show_error("Loading template...")

        try:
            # Inspect the template
            inspector = TemplateInspector(template_source)
            options, context = inspector.inspect()

            if not options:
                self._show_error("This template has no options with choices to test")
                return

            # Dismiss this screen and return the results
            self.dismiss((template_source, options, context))

        except FileNotFoundError as e:
            self._show_error(f"Template not found: {e}")
        except ValueError as e:
            self._show_error(f"Invalid template: {e}")
        except Exception as e:
            self._show_error(f"Error loading template: {e}")

    @on(Button.Pressed, "#quit-btn")
    def handle_quit(self) -> None:
        """Handle quit button press."""
        self.app.exit()

    @on(Input.Submitted)
    def handle_input_submitted(self) -> None:
        """Handle Enter key in input field."""
        self.query_one("#continue-btn", Button).press()

    def _show_error(self, message: str) -> None:
        """
        Show an error message.

        Args:
            message: The error message to display.

        """
        error_widget = self.query_one("#error", Static)
        error_widget.update(message)
