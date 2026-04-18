"""Tests for combination generation."""

import pytest

from cookie_taster.core.combinations import (
    estimate_combination_count,
    generate_combinations,
)
from cookie_taster.core.template import TemplateOption


def test_generate_combinations_single_option():
    """Test generating combinations with a single option."""
    options = [
        TemplateOption("db", ["postgres", "mysql"], "postgres"),
    ]
    selections = {"db": ["postgres", "mysql"]}

    combinations = generate_combinations(options, selections)

    assert len(combinations) == 2
    assert {"db": "postgres"} in combinations
    assert {"db": "mysql"} in combinations


def test_generate_combinations_multiple_options():
    """Test generating combinations with multiple options."""
    options = [
        TemplateOption("db", ["postgres", "mysql"], "postgres"),
        TemplateOption("cache", ["redis", "memcached"], "redis"),
    ]
    selections = {
        "db": ["postgres", "mysql"],
        "cache": ["redis", "memcached"],
    }

    combinations = generate_combinations(options, selections)

    assert len(combinations) == 4
    assert {"db": "postgres", "cache": "redis"} in combinations
    assert {"db": "postgres", "cache": "memcached"} in combinations
    assert {"db": "mysql", "cache": "redis"} in combinations
    assert {"db": "mysql", "cache": "memcached"} in combinations


def test_generate_combinations_partial_selection():
    """Test generating combinations when only some options are selected."""
    options = [
        TemplateOption("db", ["postgres", "mysql"], "postgres"),
        TemplateOption("cache", ["redis", "memcached"], "redis"),
    ]
    selections = {
        "db": ["postgres", "mysql"],
        # cache not in selections, should use default
    }

    combinations = generate_combinations(options, selections)

    assert len(combinations) == 2
    assert {"db": "postgres", "cache": "redis"} in combinations
    assert {"db": "mysql", "cache": "redis"} in combinations


def test_generate_combinations_with_base_context():
    """Test generating combinations with base context."""
    options = [
        TemplateOption("db", ["postgres", "mysql"], "postgres"),
    ]
    selections = {"db": ["postgres", "mysql"]}
    base_context = {"project_name": "myproject", "author": "John Doe"}

    combinations = generate_combinations(options, selections, base_context)  # type: ignore[arg-type]

    assert len(combinations) == 2
    for combo in combinations:
        assert combo["project_name"] == "myproject"
        assert combo["author"] == "John Doe"
        assert combo["db"] in ["postgres", "mysql"]


def test_generate_combinations_empty_selections():
    """Test generating combinations with empty selections."""
    options = [
        TemplateOption("db", ["postgres", "mysql"], "postgres"),
        TemplateOption("cache", ["redis", "memcached"], "redis"),
    ]
    selections = {}  # type: ignore[var-annotated]

    combinations = generate_combinations(options, selections)

    # Should return one combination with all defaults
    assert len(combinations) == 1
    assert combinations[0] == {"db": "postgres", "cache": "redis"}


def test_generate_combinations_invalid_option():
    """Test that invalid option names raise ValueError."""
    options = [
        TemplateOption("db", ["postgres", "mysql"], "postgres"),
    ]
    selections = {"invalid_option": ["value"]}

    with pytest.raises(ValueError, match="Unknown option"):
        generate_combinations(options, selections)


def test_generate_combinations_invalid_value():
    """Test that invalid values raise ValueError."""
    options = [
        TemplateOption("db", ["postgres", "mysql"], "postgres"),
    ]
    selections = {"db": ["postgres", "invalid_db"]}

    with pytest.raises(ValueError, match="Invalid values"):
        generate_combinations(options, selections)


def test_estimate_combination_count():
    """Test estimating combination count."""
    options = [
        TemplateOption("db", ["postgres", "mysql", "sqlite"], "postgres"),
        TemplateOption("cache", ["redis", "memcached"], "redis"),
    ]
    selections = {
        "db": ["postgres", "mysql", "sqlite"],
        "cache": ["redis", "memcached"],
    }

    count = estimate_combination_count(options, selections)
    assert count == 6  # 3 * 2


def test_estimate_combination_count_partial():
    """Test estimating combination count with partial selections."""
    options = [
        TemplateOption("db", ["postgres", "mysql", "sqlite"], "postgres"),
        TemplateOption("cache", ["redis", "memcached"], "redis"),
    ]
    selections = {
        "db": ["postgres", "mysql"],
        # cache not selected
    }

    count = estimate_combination_count(options, selections)
    assert count == 2  # Only 2 db options selected
