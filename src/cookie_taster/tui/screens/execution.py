"""Execution and results screen."""

import asyncio
from pathlib import Path

from rich.table import Table
from textual import work
from textual.app import ComposeResult
from textual.containers import Center, Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, ProgressBar, Static

from cookie_taster.core.combinations import generate_combinations
from cookie_taster.core.generator import ProjectGenerator
from cookie_taster.core.template import TemplateOption
from cookie_taster.plugins.manager import PluginManager
from cookie_taster.plugins.models import TasterStatus, TemplateMetadata


class ExecutionScreen(Screen[None]):
    """Screen for showing execution progress and results."""

    CSS = """
    ExecutionScreen {
        align: center top;
    }

    #execution-container {
        width: 95%;
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

    #status {
        text-align: center;
        color: $text-muted;
        margin-bottom: 1;
    }

    ProgressBar {
        margin-bottom: 2;
    }

    #results-area {
        height: 1fr;
        margin-bottom: 1;
    }

    #buttons {
        align: center middle;
    }

    Button {
        margin: 0 1;
    }

    .status-success {
        color: $success;
    }

    .status-failure {
        color: $error;
    }

    .status-error {
        color: $warning;
    }
    """

    def __init__(
        self,
        template_source: str,
        options: list[TemplateOption],
        selections: dict[str, list[str]],
        output_dir: Path,
        base_context: dict[str, object] | None = None,
    ) -> None:
        """
        Initialize the execution screen.

        Args:
            template_source: The template source.
            options: List of template options.
            selections: Selected values for each option.
            output_dir: Directory to generate projects in.
            base_context: Base context with all template variables.

        """
        super().__init__()
        self.template_source = template_source
        self.options = options
        self.selections = selections
        self.output_dir = output_dir
        self.base_context = base_context
        self.results: list[tuple[dict[str, str], bool, list[str]]] = []

    def compose(self) -> ComposeResult:
        """Compose the UI."""
        yield Header()
        with Vertical(id="execution-container"):
            yield Static("Generating & Testing Projects", id="title")
            yield Static("Initializing...", id="status")
            yield ProgressBar(total=100, show_eta=True, id="progress")
            with VerticalScroll(id="results-area"):
                yield Static("", id="results-table")
            with Center(id="buttons"):
                yield Button("Done", variant="primary", id="done-btn", disabled=True)
        yield Footer()

    def on_mount(self) -> None:
        """Handle screen mount."""
        self._start_execution()

    @work(exclusive=True)
    async def _start_execution(self) -> None:
        """Start the execution process."""
        status_widget = self.query_one("#status", Static)
        progress_bar = self.query_one("#progress", ProgressBar)

        # Generate combinations
        status_widget.update("Generating combinations...")
        combinations = generate_combinations(
            self.options, self.selections, self.base_context
        )

        total_steps = len(combinations) * 2  # Generate + Test
        progress_bar.update(total=total_steps)

        # Initialize plugin manager
        plugin_manager = PluginManager()
        plugin_manager.load_plugins()

        # Create project generator
        template_metadata = TemplateMetadata(source=self.template_source)
        generator = ProjectGenerator(
            self.template_source,
            self.output_dir,
            template_metadata,
        )

        current_step = 0

        # Generate and test each project
        for i, context in enumerate(combinations, 1):
            # Generate project
            status_widget.update(
                f"Generating project {i}/{len(combinations)}: "
                f"{self._format_context(context)}"
            )

            result = generator.generate(context)
            current_step += 1
            progress_bar.update(progress=current_step)

            if not result.success or result.project_path is None:
                self.results.append(
                    (context, False, [f"Generation failed: {result.error}"])
                )
                self._update_results_table()
                continue

            # Test project
            status_widget.update(
                f"Testing project {i}/{len(combinations)}: "
                f"{self._format_context(context)}"
            )

            project_info = generator.generate_with_info(context)
            if project_info:
                taster_results = plugin_manager.run_tasters(project_info)

                # Collect results
                success = all(r.status == TasterStatus.SUCCESS for r in taster_results)
                messages = [f"{r.taster_name}: {r.message}" for r in taster_results]
                self.results.append((context, success, messages))
            else:
                self.results.append((context, False, ["Failed to create project info"]))

            current_step += 1
            progress_bar.update(progress=current_step)
            self._update_results_table()

            # Small delay to allow UI to update
            await asyncio.sleep(0.1)

        # Done
        status_widget.update("Execution complete!")
        done_btn = self.query_one("#done-btn", Button)
        done_btn.disabled = False

    def _format_context(self, context: dict[str, str]) -> str:
        """
        Format context for display.

        Args:
            context: The context dictionary.

        Returns:
            A formatted string.

        """
        # Show only the variable options (not the full context)
        option_names = [opt.name for opt in self.options]
        relevant = {k: v for k, v in context.items() if k in option_names}
        return ", ".join(f"{k}={v}" for k, v in relevant.items())

    def _update_results_table(self) -> None:
        """Update the results table."""
        table = Table(title="Results", expand=True)
        table.add_column("Configuration", style="cyan")
        table.add_column("Status", style="bold")
        table.add_column("Details")

        for context, success, messages in self.results:
            config = self._format_context(context)
            status = "✓ PASS" if success else "✗ FAIL"
            status_style = "green" if success else "red"
            details = "\n".join(messages) if messages else "No details"

            table.add_row(
                config,
                f"[{status_style}]{status}[/{status_style}]",
                details,
            )

        results_widget = self.query_one("#results-table", Static)
        results_widget.update(table)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "done-btn":
            self.app.exit()
