"""Example taster to demonstrate the plugin API."""

import time

import pluggy

from cookie_taster.plugins.models import (
    ProjectInfo,
    TasterContext,
    TasterResult,
    TasterStatus,
)

hookimpl = pluggy.HookimplMarker("cookie_taster")


class ExampleTaster:
    """
    An example taster that checks for basic project structure.

    This taster demonstrates:
    - How to implement the taster hooks
    - How to check context to determine if the taster should run
    - How to inspect the generated project
    - How to return results with logs

    """

    @hookimpl
    def get_taster_name(self) -> str:
        """Return the name of this taster."""
        return "example"

    @hookimpl
    def can_handle(self, context: TasterContext) -> bool:
        """
        Determine if this taster can handle the project.

        This example taster runs on all projects, but real tasters
        would check the context to determine if they're applicable.

        For example:
        - A Heroku taster might check if 'use_heroku' is 'y'
        - A Docker taster might check if 'use_docker' is 'y'

        Args:
            context: Context information about the project.

        Returns:
            True if this taster can handle the project.

        """
        # This example taster runs on all projects
        return True

    @hookimpl
    def test_project(self, project_info: ProjectInfo) -> TasterResult:
        """
        Test the generated project.

        Args:
            project_info: Information about the generated project.

        Returns:
            The result of testing the project.

        """
        start_time = time.time()
        logs = []

        logs.append(f"Testing project at: {project_info.path}")
        logs.append(f"Context: {project_info.cookiecutter_context}")

        # Check if the project directory exists
        if not project_info.path.exists():
            return TasterResult(
                taster_name=self.get_taster_name(),
                status=TasterStatus.ERROR,
                message="Project directory does not exist",
                logs=logs,
                duration_seconds=time.time() - start_time,
            )

        logs.append(f"Project directory exists: {project_info.path}")

        # Check for common files
        common_files = ["README.md", "README.rst", "README.txt", "README"]
        has_readme = any(
            (project_info.path / filename).exists() for filename in common_files
        )

        if has_readme:
            logs.append("Found README file")
        else:
            logs.append("No README file found")

        # Count files in the project
        file_count = sum(1 for _ in project_info.path.rglob("*") if _.is_file())
        logs.append(f"Total files in project: {file_count}")

        # Determine status
        if file_count == 0:
            status = TasterStatus.FAILURE
            message = "Project has no files"
        elif has_readme:
            status = TasterStatus.SUCCESS
            message = f"Project structure looks good ({file_count} files)"
        else:
            status = TasterStatus.SUCCESS
            message = (
                f"Project generated successfully ({file_count} files, but no README)"
            )

        return TasterResult(
            taster_name=self.get_taster_name(),
            status=status,
            message=message,
            logs=logs,
            duration_seconds=time.time() - start_time,
        )
