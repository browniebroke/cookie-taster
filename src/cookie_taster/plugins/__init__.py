"""Plugin system for Cookie Taster."""

from cookie_taster.plugins.manager import PluginManager
from cookie_taster.plugins.models import (
    ProjectInfo,
    TasterContext,
    TasterResult,
    TasterStatus,
    TemplateMetadata,
)

__all__ = [
    "PluginManager",
    "ProjectInfo",
    "TasterContext",
    "TasterResult",
    "TasterStatus",
    "TemplateMetadata",
]
