"""Template inspection functionality."""

import json
import tempfile
from dataclasses import dataclass
from pathlib import Path

from cookiecutter.repository import determine_repo_dir


@dataclass
class TemplateOption:
    """Represents a cookiecutter template option with choices."""

    name: str
    """The variable name in the template."""

    choices: list[str]
    """Available choices for this option."""

    default: str
    """The default choice."""

    def __post_init__(self) -> None:
        """Validate the option after initialization."""
        if not self.choices:
            msg = f"Option '{self.name}' must have at least one choice"
            raise ValueError(msg)
        if self.default not in self.choices:
            msg = (
                f"Default value '{self.default}' for option '{self.name}' "
                f"is not in choices: {self.choices}"
            )
            raise ValueError(msg)


class TemplateInspector:
    """Inspects cookiecutter templates to extract configuration options."""

    def __init__(self, template_source: str) -> None:
        """
        Initialize the template inspector.

        Args:
            template_source: URL, path, or other source for the template.

        """
        self.template_source = template_source
        self._template_dir: Path | None = None
        self._context: dict[str, object] | None = None

    def inspect(self) -> tuple[list[TemplateOption], dict[str, object]]:
        """
        Inspect the template and extract options with choices.

        Returns:
            A tuple of (options_with_choices, full_context) where:
            - options_with_choices: List of options that have multiple choices
            - full_context: The complete cookiecutter.json context

        Raises:
            FileNotFoundError: If the template or cookiecutter.json cannot be found.
            ValueError: If the cookiecutter.json is invalid.

        """
        # Get the template directory
        template_dir = self._get_template_dir()

        # Load the cookiecutter.json
        context = self._load_context(template_dir)

        # Extract options with choices
        options = self._extract_options(context)

        return options, context

    def _get_template_dir(self) -> Path:
        """
        Get the template directory, cloning if necessary.

        Returns:
            Path to the template directory.

        """
        if self._template_dir is None:
            # Use cookiecutter's determine_repo_dir to handle various sources
            # (Git URLs, local paths, etc.)
            with tempfile.TemporaryDirectory() as clone_dir:
                repo_dir, _ = determine_repo_dir(
                    template=self.template_source,
                    abbreviations={},
                    clone_to_dir=clone_dir,
                    checkout=None,
                    no_input=True,
                )
                # Convert to Path and store
                self._template_dir = Path(repo_dir).resolve()

        return self._template_dir

    def _load_context(self, template_dir: Path) -> dict[str, object]:
        """
        Load the cookiecutter.json file from the template.

        Args:
            template_dir: Path to the template directory.

        Returns:
            The parsed cookiecutter.json context.

        Raises:
            FileNotFoundError: If cookiecutter.json doesn't exist.
            ValueError: If the JSON is invalid.

        """
        if self._context is not None:
            return self._context

        context_file = template_dir / "cookiecutter.json"

        if not context_file.exists():
            msg = f"cookiecutter.json not found in {template_dir}"
            raise FileNotFoundError(msg)

        try:
            with context_file.open() as f:
                self._context = json.load(f)
        except json.JSONDecodeError as e:
            msg = f"Invalid JSON in cookiecutter.json: {e}"
            raise ValueError(msg) from e

        return self._context

    def _extract_options(self, context: dict[str, object]) -> list[TemplateOption]:
        """
        Extract options that have multiple choices.

        Args:
            context: The cookiecutter.json context.

        Returns:
            List of options with choices.

        """
        options = []

        for key, value in context.items():
            # Check if the value is a list (indicates choices)
            if isinstance(value, list) and len(value) > 0:
                # First item is the default
                default = str(value[0])
                choices = [str(choice) for choice in value]

                try:
                    option = TemplateOption(
                        name=key,
                        choices=choices,
                        default=default,
                    )
                    options.append(option)
                except ValueError:
                    # Skip invalid options
                    continue

        return options

    @property
    def template_dir(self) -> Path | None:
        """
        Get the template directory if it has been loaded.

        Returns:
            The template directory path or None if not yet loaded.

        """
        return self._template_dir
