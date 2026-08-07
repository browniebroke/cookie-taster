"""Project generation using cookiecutter."""

import shutil
from dataclasses import dataclass
from pathlib import Path

from cookiecutter.main import cookiecutter

from cookie_taster.plugins.models import ProjectInfo, TemplateMetadata


@dataclass
class GenerationResult:
    """Result of generating a project."""

    success: bool
    """Whether the generation succeeded."""

    project_path: Path | None = None
    """Path to the generated project (if successful)."""

    error: str | None = None
    """Error message (if failed)."""

    context: dict[str, str] | None = None
    """The context used for generation."""


class ProjectGenerator:
    """Generates projects from cookiecutter templates."""

    def __init__(
        self,
        template_source: str,
        output_dir: Path,
        template_metadata: TemplateMetadata | None = None,
    ) -> None:
        """
        Initialize the project generator.

        Args:
            template_source: URL or path to the cookiecutter template.
            output_dir: Directory where projects will be generated.
            template_metadata: Optional metadata about the template.

        """
        self.template_source = template_source
        self.output_dir = output_dir
        self.template_metadata = template_metadata or TemplateMetadata(
            source=template_source
        )

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, context: dict[str, str]) -> GenerationResult:
        """
        Generate a project with the given context.

        Args:
            context: Cookiecutter context (variable values).

        Returns:
            Result of the generation.

        """
        try:
            # Generate the project using cookiecutter
            project_path = cookiecutter(
                template=self.template_source,
                output_dir=str(self.output_dir),
                no_input=True,
                extra_context=context,
            )

            return GenerationResult(
                success=True,
                project_path=Path(project_path),
                context=context,
            )

        except Exception as e:
            return GenerationResult(
                success=False,
                error=str(e),
                context=context,
            )

    def generate_with_info(self, context: dict[str, str]) -> ProjectInfo | None:
        """
        Generate a project and return ProjectInfo if successful.

        Args:
            context: Cookiecutter context (variable values).

        Returns:
            ProjectInfo if generation succeeded, None otherwise.

        """
        result = self.generate(context)

        if result.success and result.project_path:
            return ProjectInfo(
                path=result.project_path,
                cookiecutter_context=context,
                template_metadata=self.template_metadata,
            )

        return None

    def generate_batch(self, contexts: list[dict[str, str]]) -> list[GenerationResult]:
        """
        Generate multiple projects in batch.

        Args:
            contexts: List of cookiecutter contexts to generate.

        Returns:
            List of generation results.

        """
        results = []
        for context in contexts:
            result = self.generate(context)
            results.append(result)

        return results

    def cleanup_project(self, project_path: Path) -> bool:
        """
        Remove a generated project.

        Args:
            project_path: Path to the project to remove.

        Returns:
            True if cleanup succeeded, False otherwise.

        """
        try:
            if project_path.exists():
                shutil.rmtree(project_path)
            return True
        except Exception:
            return False

    def cleanup_all(self) -> None:
        """Remove all generated projects in the output directory."""
        if self.output_dir.exists():
            for item in self.output_dir.iterdir():
                if item.is_dir():
                    self.cleanup_project(item)
