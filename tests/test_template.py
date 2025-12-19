"""Tests for template inspection."""

import pytest

from cookie_taster.core.template import TemplateOption


def test_template_option_creation():
    """Test creating a TemplateOption."""
    option = TemplateOption(
        name="database",
        choices=["postgres", "mysql", "sqlite"],
        default="postgres",
    )

    assert option.name == "database"
    assert option.choices == ["postgres", "mysql", "sqlite"]
    assert option.default == "postgres"


def test_template_option_validation_empty_choices():
    """Test that empty choices raise ValueError."""
    with pytest.raises(ValueError, match="must have at least one choice"):
        TemplateOption(name="database", choices=[], default="postgres")


def test_template_option_validation_invalid_default():
    """Test that invalid default raises ValueError."""
    with pytest.raises(ValueError, match="is not in choices"):
        TemplateOption(
            name="database",
            choices=["postgres", "mysql"],
            default="sqlite",  # Not in choices
        )


def test_template_option_default_in_choices():
    """Test that default must be in choices."""
    option = TemplateOption(
        name="database",
        choices=["postgres", "mysql", "sqlite"],
        default="mysql",  # Valid choice
    )

    assert option.default == "mysql"
    assert "mysql" in option.choices
