"""Plugin manager for taster plugins."""

from typing import Any

import pluggy

from cookie_taster.plugins import hookspecs
from cookie_taster.plugins.models import ProjectInfo, TasterContext, TasterResult


class PluginManager:
    """Manager for taster plugins."""

    def __init__(self) -> None:
        """Initialize the plugin manager."""
        self.pm = pluggy.PluginManager("cookie_taster")
        self.pm.add_hookspecs(hookspecs)

    def load_plugins(self) -> None:
        """Load all available taster plugins from entry points."""
        self.pm.load_setuptools_entrypoints("cookie_taster.tasters")

    def register_plugin(self, plugin: Any, name: str | None = None) -> None:
        """
        Register a plugin instance directly.

        Args:
            plugin: The plugin instance to register.
            name: Optional name for the plugin.

        """
        self.pm.register(plugin, name=name)

    def get_taster_names(self) -> list[str]:
        """
        Get names of all registered tasters.

        Returns:
            List of taster names.

        """
        results = self.pm.hook.get_taster_name()
        return [name for name in results if name]

    def get_applicable_tasters(self, context: TasterContext) -> list[str]:
        """
        Get names of tasters that can handle the given context.

        Args:
            context: The context to check.

        Returns:
            List of taster names that can handle this context.

        """
        names = self.get_taster_names()
        can_handle_results = self.pm.hook.can_handle(context=context)

        applicable = []
        for name, can_handle in zip(names, can_handle_results, strict=True):
            if can_handle:
                applicable.append(name)

        return applicable

    def run_tasters(
        self, project_info: ProjectInfo, taster_names: list[str] | None = None
    ) -> list[TasterResult]:
        """
        Run tasters on a project.

        Args:
            project_info: Information about the project to test.
            taster_names: Optional list of specific taster names to run.
                If None, runs all applicable tasters.

        Returns:
            List of results from running the tasters.

        """
        # If no specific tasters requested, find all applicable ones
        if taster_names is None:
            taster_names = self.get_applicable_tasters(project_info.taster_context)

        # Get all taster names and results
        all_names = self.get_taster_names()
        all_results = self.pm.hook.test_project(project_info=project_info)

        # Filter results to only include requested/applicable tasters
        filtered_results = []
        for name, result in zip(all_names, all_results, strict=True):
            if name in taster_names:
                filtered_results.append(result)

        return filtered_results

    @property
    def plugin_count(self) -> int:
        """
        Get the number of registered plugins.

        Returns:
            The number of plugins.

        """
        return len(self.pm.get_plugins())
