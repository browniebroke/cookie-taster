# Cookie Taster

<p align="center">
  <a href="https://github.com/browniebroke/cookie-taster/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/browniebroke/cookie-taster/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://cookie-taster.readthedocs.io">
    <img src="https://img.shields.io/readthedocs/cookie-taster.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">
  </a>
  <a href="https://codecov.io/gh/browniebroke/cookie-taster">
    <img src="https://img.shields.io/codecov/c/github/browniebroke/cookie-taster.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/cookie-taster/">
    <img src="https://img.shields.io/pypi/v/cookie-taster.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/cookie-taster.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/cookie-taster.svg?style=flat-square" alt="License">
</p>

---

**Documentation**: <a href="https://cookie-taster.readthedocs.io" target="_blank">https://cookie-taster.readthedocs.io </a>

**Source Code**: <a href="https://github.com/browniebroke/cookie-taster" target="_blank">https://github.com/browniebroke/cookie-taster </a>

---

A tool to test cookiecutter templates in parallel by generating all combinations of template options.

## What is Cookie Taster?

Cookie Taster helps you thoroughly test your [cookiecutter](https://www.cookiecutter.io) templates by:

- 🔍 Automatically detecting all choice-based options in your template
- 🎯 Letting you select multiple values for each option
- 🚀 Generating all combinations of projects in parallel
- ✅ Running customizable "tasters" to validate each generated project
- 📊 Providing a beautiful TUI (Terminal User Interface) to monitor progress

Perfect for template maintainers who want to ensure all option combinations work correctly!

## Installation

Install this via pip (or your favourite package manager):

```bash
pip install cookie-taster
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv tool install cookie-taster
```

## Quick Start

Launch the interactive TUI:

```bash
cookie-taster test
```

Or provide a template directly:

```bash
cookie-taster test https://github.com/cookiecutter/cookiecutter-django
```

Specify a custom output directory:

```bash
cookie-taster test -o ./my-test-projects
```

## How It Works

1. **Template Input**: Provide a cookiecutter template (URL, local path, or any source cookiecutter accepts)
2. **Option Selection**: Choose multiple values for each template option with choices
3. **Generation & Testing**: Watch as Cookie Taster generates all combinations and runs tasters on each
4. **Results**: Review which combinations passed and which failed

## Creating Custom Tasters

Tasters are plugins that validate generated projects. Create your own to test specific aspects of your templates!

### Example Taster

```python
"""Example custom taster."""
import pluggy
from cookie_taster.plugins.models import (
    ProjectInfo,
    TasterContext,
    TasterResult,
    TasterStatus,
)

hookimpl = pluggy.HookimplMarker("cookie_taster")

class MyCustomTaster:
    @hookimpl
    def get_taster_name(self) -> str:
        return "my-custom-taster"

    @hookimpl
    def can_handle(self, context: TasterContext) -> bool:
        # Only run if specific option is selected
        return context.cookiecutter_context.get("use_docker") == "y"

    @hookimpl
    def test_project(self, project_info: ProjectInfo) -> TasterResult:
        # Validate the generated project
        dockerfile = project_info.path / "Dockerfile"

        if dockerfile.exists():
            return TasterResult(
                taster_name=self.get_taster_name(),
                status=TasterStatus.SUCCESS,
                message="Dockerfile exists",
            )
        else:
            return TasterResult(
                taster_name=self.get_taster_name(),
                status=TasterStatus.FAILURE,
                message="Dockerfile missing",
            )
```

### Installing Your Taster

Register your taster as a plugin entry point in `pyproject.toml`:

```toml
[project.entry-points."cookie_taster.tasters"]
my_custom = "my_package.tasters:MyCustomTaster"
```

Cookie Taster will automatically discover and load your taster!

## Use Cases

### Testing cookiecutter-django

```bash
cookie-taster test https://github.com/cookiecutter/cookiecutter-django
```

Select multiple options for:

- Cloud providers (AWS, GCP, Azure, etc.)
- Database options (PostgreSQL, MySQL)
- CI systems (GitHub Actions, GitLab CI)
- And more!

Create tasters to validate:

- Docker configurations for each platform
- CI pipeline files
- Database setup scripts
- Deployment configurations

### Validating Your Own Templates

Ensure all option combinations in your template work correctly:

1. Run Cookie Taster with your template
2. Select all options you want to test
3. Create custom tasters for your specific validation needs
4. Get a comprehensive report of what works and what doesn't

## Features

- ✨ **Interactive TUI** - Beautiful terminal interface powered by [Textual](https://textual.textualize.io/)
- 🔌 **Plugin System** - Extensible taster plugins using [pluggy](https://pluggy.readthedocs.io/)
- ⚡ **Parallel Generation** - Generate multiple projects efficiently
- 📋 **Combination Explosion** - Automatically creates all permutations of your selections
- 🎯 **Smart Tasters** - Tasters can decide which projects they can handle
- 📊 **Real-time Progress** - Watch generation and testing progress live

## Requirements

- Python 3.10 or higher
- cookiecutter 2.6+

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- prettier-ignore-start -->
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://browniebroke.com/"><img src="https://avatars.githubusercontent.com/u/861044?v=4?s=80" width="80px;" alt="Bruno Alla"/><br /><sub><b>Bruno Alla</b></sub></a><br /><a href="https://github.com/browniebroke/cookie-taster/commits?author=browniebroke" title="Code">💻</a> <a href="#ideas-browniebroke" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/browniebroke/cookie-taster/commits?author=browniebroke" title="Documentation">📖</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-end -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)

This package was created with
[Copier](https://copier.readthedocs.io/) and the
[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)
project template.
