"""Core functionality for Cookie Taster."""

from cookie_taster.core.combinations import (
    estimate_combination_count,
    generate_combinations,
)
from cookie_taster.core.generator import GenerationResult, ProjectGenerator
from cookie_taster.core.template import TemplateInspector, TemplateOption

__all__ = [
    "GenerationResult",
    "ProjectGenerator",
    "TemplateInspector",
    "TemplateOption",
    "estimate_combination_count",
    "generate_combinations",
]
