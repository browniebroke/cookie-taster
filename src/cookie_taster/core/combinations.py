"""Combination generation for template options."""

from itertools import product

from cookie_taster.core.template import TemplateOption


def generate_combinations(
    options: list[TemplateOption],
    selections: dict[str, list[str]],
    base_context: dict[str, object] | None = None,
) -> list[dict[str, str]]:
    """
    Generate all combinations of selected options.

    Args:
        options: List of template options with choices.
        selections: Dictionary mapping option names to selected values.
            Only options in this dict will be varied; others use defaults.
        base_context: Optional base context with default values for all variables.

    Returns:
        List of context dictionaries, one for each combination.

    Raises:
        ValueError: If selections reference unknown options or invalid choices.

    Examples:
        >>> options = [
        ...     TemplateOption("db", ["postgres", "mysql"], "postgres"),
        ...     TemplateOption("cache", ["redis", "memcached"], "redis"),
        ... ]
        >>> selections = {
        ...     "db": ["postgres", "mysql"],
        ...     "cache": ["redis"],
        ... }
        >>> combinations = generate_combinations(options, selections)
        >>> len(combinations)
        2
        >>> combinations[0]
        {'db': 'postgres', 'cache': 'redis'}
        >>> combinations[1]
        {'db': 'mysql', 'cache': 'redis'}

    """
    # Validate selections
    option_map = {opt.name: opt for opt in options}

    for option_name, selected_values in selections.items():
        if option_name not in option_map:
            msg = f"Unknown option: {option_name}"
            raise ValueError(msg)

        option = option_map[option_name]
        invalid_values = [v for v in selected_values if v not in option.choices]
        if invalid_values:
            msg = (
                f"Invalid values for option '{option_name}': {invalid_values}. "
                f"Valid choices: {option.choices}"
            )
            raise ValueError(msg)

    # Build the base context (with defaults)
    if base_context is None:
        base_context = {}

    # For options with selections, prepare lists of values to vary
    # For options without selections, use the default value
    varying_options = []
    varying_values = []

    for option in options:
        if option.name in selections and len(selections[option.name]) > 0:
            varying_options.append(option.name)
            varying_values.append(selections[option.name])

    # If no selections were made, return a single combination with defaults
    if not varying_options:
        result_context = dict(base_context)
        for option in options:
            result_context[option.name] = option.default
        return [result_context]  # type: ignore[list-item]

    # Generate all combinations using itertools.product
    combinations = []
    for value_tuple in product(*varying_values):
        # Start with the base context
        combo_context = dict(base_context)

        # Apply the varying values
        for option_name, value in zip(varying_options, value_tuple, strict=True):
            combo_context[option_name] = value

        # Add defaults for options not in selections
        for option in options:
            if option.name not in selections or len(selections[option.name]) == 0:
                combo_context[option.name] = option.default

        combinations.append(combo_context)

    return combinations  # type: ignore[return-value]


def estimate_combination_count(
    options: list[TemplateOption], selections: dict[str, list[str]]
) -> int:
    """
    Estimate the number of combinations that will be generated.

    Args:
        options: List of template options with choices.
        selections: Dictionary mapping option names to selected values.

    Returns:
        The number of combinations that will be generated.

    """
    option_map = {opt.name: opt for opt in options}

    count = 1
    for option_name, selected_values in selections.items():
        if option_name in option_map and len(selected_values) > 0:
            count *= len(selected_values)

    return count
