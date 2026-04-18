"""Hook specifications for Cookie Taster plugins."""

import pluggy

from cookie_taster.plugins.models import ProjectInfo, TasterContext, TasterResult

hookspec = pluggy.HookspecMarker("cookie_taster")


@hookspec
def get_taster_name() -> str:  # type: ignore[empty-body]
    """
    Return the name of the taster.

    Returns:
        A human-readable name for this taster.

    """


@hookspec
def can_handle(context: TasterContext) -> bool:  # type: ignore[empty-body]
    """
    Determine if this taster can handle the given project.

    Args:
        context: Context information about the project and template.

    Returns:
        True if this taster can handle the project, False otherwise.

    """


@hookspec
def test_project(project_info: ProjectInfo) -> TasterResult:  # type: ignore[empty-body]
    """
    Execute tests on the generated project.

    Args:
        project_info: Information about the generated project.

    Returns:
        The result of running the taster.

    """
