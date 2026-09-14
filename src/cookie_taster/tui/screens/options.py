"""Options selection screen."""

from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Checkbox, Footer, Header, Label, Static

from cookie_taster.core.combinations import estimate_combination_count
from cookie_taster.core.template import TemplateOption


class OptionGroup(Vertical):
    """A group of checkboxes for a single option."""

    def __init__(self, option: TemplateOption) -> None:
        """
        Initialize the option group.

        Args:
            option: The template option to display.

        """
        super().__init__(classes="option-group")
        self.option = option

    def compose(self) -> ComposeResult:
        """Compose the option group."""
        yield Label(f"[b]{self.option.name}[/b]", classes="option-label")
        for choice in self.option.choices:
            is_default = choice == self.option.default
            checkbox = Checkbox(
                choice,
                value=is_default,
                id=f"checkbox-{self.option.name}-{choice}",
            )
            checkbox.border_title = None
            yield checkbox


class OptionsScreen(Screen[dict[str, list[str]]]):
    """Screen for selecting multiple values for each option."""

    CSS = """
    OptionsScreen {
        align: center top;
    }

    #options-container {
        width: 90;
        height: 90%;
        border: solid $primary;
        padding: 1 2;
        margin: 1;
    }

    #title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }

    #description {
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
    }

    #combination-count {
        text-align: center;
        color: $accent;
        margin-bottom: 2;
        text-style: bold;
    }

    .option-group {
        border: solid $panel;
        padding: 1 2;
        margin-bottom: 1;
    }

    .option-label {
        margin-bottom: 1;
    }

    #buttons {
        align: center middle;
        margin-top: 1;
    }

    Button {
        margin: 0 1;
    }

    #scroll-area {
        height: 1fr;
    }
    """

    def __init__(self, options: list[TemplateOption]) -> None:
        """
        Initialize the options screen.

        Args:
            options: List of template options with choices.

        """
        super().__init__()
        self.options = options

    def compose(self) -> ComposeResult:
        """Compose the UI."""
        yield Header()
        with Vertical(id="options-container"):
            yield Static("Select Options", id="title")
            yield Static(
                "Choose multiple values for each option to test combinations",
                id="description",
            )
            yield Static("", id="combination-count")
            with VerticalScroll(id="scroll-area"):
                for option in self.options:
                    yield OptionGroup(option)
            with Center(id="buttons"):
                yield Button("Generate Projects", variant="primary", id="generate-btn")
                yield Button("Back", variant="default", id="back-btn")
        yield Footer()

    def on_mount(self) -> None:
        """Handle screen mount."""
        self._update_combination_count()

    @on(Checkbox.Changed)
    def handle_checkbox_changed(self) -> None:
        """Handle checkbox state changes."""
        self._update_combination_count()

    @on(Button.Pressed, "#generate-btn")
    def handle_generate(self) -> None:
        """Handle generate button press."""
        selections = self._get_selections()

        # Validate that at least one option is selected for each variable
        if not selections:
            return

        # Check if at least one checkbox is checked per option
        for option in self.options:
            if option.name not in selections or len(selections[option.name]) == 0:
                # If nothing selected, use default
                selections[option.name] = [option.default]

        self.dismiss(selections)

    @on(Button.Pressed, "#back-btn")
    def handle_back(self) -> None:
        """Handle back button press."""
        self.app.pop_screen()

    def _get_selections(self) -> dict[str, list[str]]:
        """
        Get the current selections.

        Returns:
            Dictionary mapping option names to selected values.

        """
        selections: dict[str, list[str]] = {}

        for option_group in self.query(OptionGroup):
            option_name = option_group.option.name
            selected_values = []

            # Find all checkboxes for this option
            for checkbox in option_group.query(Checkbox):
                if checkbox.value:
                    # Extract the choice from the checkbox label
                    choice = checkbox.label.plain
                    selected_values.append(choice)

            if selected_values:
                selections[option_name] = selected_values

        return selections

    def _update_combination_count(self) -> None:
        """Update the combination count display."""
        selections = self._get_selections()

        # Make sure empty selections use defaults
        for option in self.options:
            if option.name not in selections or len(selections[option.name]) == 0:
                selections[option.name] = [option.default]

        count = estimate_combination_count(self.options, selections)

        count_widget = self.query_one("#combination-count", Static)
        count_widget.update(f"This will generate {count} project(s)")
