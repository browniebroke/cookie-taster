"""Tests for plugin models."""

from cookie_taster.plugins.models import (
    ProjectInfo,
    TasterContext,
    TasterResult,
    TasterStatus,
    TemplateMetadata,
)


def test_template_metadata_creation():
    """Test creating TemplateMetadata."""
    metadata = TemplateMetadata(
        source="https://github.com/user/template",
        name="My Template",
        version="1.0.0",
    )

    assert metadata.source == "https://github.com/user/template"
    assert metadata.name == "My Template"
    assert metadata.version == "1.0.0"


def test_template_metadata_minimal():
    """Test creating TemplateMetadata with minimal info."""
    metadata = TemplateMetadata(source="/path/to/template")

    assert metadata.source == "/path/to/template"
    assert metadata.name is None
    assert metadata.version is None


def test_taster_context_creation():
    """Test creating TasterContext."""
    metadata = TemplateMetadata(source="test")
    context = TasterContext(
        cookiecutter_context={"db": "postgres", "cache": "redis"},
        template_metadata=metadata,
    )

    assert context.cookiecutter_context == {"db": "postgres", "cache": "redis"}
    assert context.template_metadata == metadata


def test_project_info_creation(tmp_path):
    """Test creating ProjectInfo."""
    path = tmp_path / "project"
    metadata = TemplateMetadata(source="test")
    project_info = ProjectInfo(
        path=path,
        cookiecutter_context={"db": "postgres"},
        template_metadata=metadata,
    )

    assert project_info.path == path
    assert project_info.cookiecutter_context == {"db": "postgres"}
    assert project_info.template_metadata == metadata


def test_project_info_taster_context(tmp_path):
    """Test getting TasterContext from ProjectInfo."""
    path = tmp_path / "project"
    metadata = TemplateMetadata(source="test")
    project_info = ProjectInfo(
        path=path,
        cookiecutter_context={"db": "postgres"},
        template_metadata=metadata,
    )

    context = project_info.taster_context

    assert isinstance(context, TasterContext)
    assert context.cookiecutter_context == {"db": "postgres"}
    assert context.template_metadata == metadata


def test_taster_result_creation():
    """Test creating TasterResult."""
    result = TasterResult(
        taster_name="example",
        status=TasterStatus.SUCCESS,
        message="All tests passed",
        logs=["Log line 1", "Log line 2"],
        duration_seconds=1.5,
    )

    assert result.taster_name == "example"
    assert result.status == TasterStatus.SUCCESS
    assert result.message == "All tests passed"
    assert result.logs == ["Log line 1", "Log line 2"]
    assert result.duration_seconds == 1.5


def test_taster_result_status_checks():
    """Test TasterResult status check methods."""
    success_result = TasterResult(
        taster_name="test",
        status=TasterStatus.SUCCESS,
    )
    assert success_result.is_success()
    assert not success_result.is_failure()
    assert not success_result.is_skipped()
    assert not success_result.is_error()

    failure_result = TasterResult(
        taster_name="test",
        status=TasterStatus.FAILURE,
    )
    assert not failure_result.is_success()
    assert failure_result.is_failure()
    assert not failure_result.is_skipped()
    assert not failure_result.is_error()

    skipped_result = TasterResult(
        taster_name="test",
        status=TasterStatus.SKIPPED,
    )
    assert not skipped_result.is_success()
    assert not skipped_result.is_failure()
    assert skipped_result.is_skipped()
    assert not skipped_result.is_error()

    error_result = TasterResult(
        taster_name="test",
        status=TasterStatus.ERROR,
    )
    assert not error_result.is_success()
    assert not error_result.is_failure()
    assert not error_result.is_skipped()
    assert error_result.is_error()


def test_taster_result_defaults():
    """Test TasterResult default values."""
    result = TasterResult(
        taster_name="test",
        status=TasterStatus.SUCCESS,
    )

    assert result.message == ""
    assert result.logs == []
    assert result.duration_seconds == 0.0
