"""Data models for the plugin system."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class TasterStatus(str, Enum):
    """Status of a taster execution."""

    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class TemplateMetadata:
    """Metadata about a cookiecutter template."""

    source: str
    """The original template source (URL, path, etc.)."""

    name: str | None = None
    """The template name if available."""

    version: str | None = None
    """The template version if available."""


@dataclass
class TasterContext:
    """
    Context provided to tasters for decision making.

    This is used by tasters to determine if they can handle a project.
    """

    cookiecutter_context: dict[str, str]
    """The cookiecutter variables and their selected values."""

    template_metadata: TemplateMetadata
    """Metadata about the template."""


@dataclass
class ProjectInfo:
    """Information about a generated project."""

    path: Path
    """Path to the generated project directory."""

    cookiecutter_context: dict[str, str]
    """The cookiecutter variables and their selected values."""

    template_metadata: TemplateMetadata
    """Metadata about the template."""

    @property
    def taster_context(self) -> TasterContext:
        """Get the taster context from project info."""
        return TasterContext(
            cookiecutter_context=self.cookiecutter_context,
            template_metadata=self.template_metadata,
        )


@dataclass
class TasterResult:
    """Result from running a taster on a project."""

    taster_name: str
    """Name of the taster that produced this result."""

    status: TasterStatus
    """Status of the taster execution."""

    message: str = ""
    """Human-readable message about the result."""

    logs: list[str] = field(default_factory=list)
    """Detailed logs from the taster execution."""

    duration_seconds: float = 0.0
    """How long the taster took to execute."""

    def is_success(self) -> bool:
        """Check if the taster succeeded."""
        return self.status == TasterStatus.SUCCESS

    def is_failure(self) -> bool:
        """Check if the taster failed."""
        return self.status == TasterStatus.FAILURE

    def is_skipped(self) -> bool:
        """Check if the taster was skipped."""
        return self.status == TasterStatus.SKIPPED

    def is_error(self) -> bool:
        """Check if the taster encountered an error."""
        return self.status == TasterStatus.ERROR
