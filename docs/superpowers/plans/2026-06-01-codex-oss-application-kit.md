# codex-oss-application-kit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a real Python CLI open-source project that helps maintainers prepare truthful Codex for Open Source application drafts.

**Architecture:** The project uses a Python `src/` layout with small modules for loading YAML, normalizing data, checking completeness, rendering Markdown, and handling CLI commands. The first release is offline-only and intentionally avoids authenticated GitHub or OpenAI form automation.

**Tech Stack:** Python 3.10+, PyYAML, pytest, standard library `argparse`, `dataclasses`, and `pathlib`.

---

## File Structure

- `pyproject.toml`: package metadata, dependencies, console script, pytest settings.
- `src/codex_oss_kit/__init__.py`: package version export.
- `src/codex_oss_kit/model.py`: `MaintainerProfile`, `ProjectProfile`, and `ApplicationProfile` dataclasses.
- `src/codex_oss_kit/loader.py`: YAML file loading and conversion to `ApplicationProfile`.
- `src/codex_oss_kit/checks.py`: required field validation and evidence warnings.
- `src/codex_oss_kit/render.py`: Markdown application draft rendering.
- `src/codex_oss_kit/cli.py`: `render` and `check` command-line interface.
- `examples/project.yml`: realistic example input for this repository.
- `tests/test_loader.py`: loader and model tests.
- `tests/test_checks.py`: validation tests.
- `tests/test_render.py`: rendering tests.
- `tests/test_cli.py`: CLI integration tests.
- `README.md`: project overview and quick start.
- `LICENSE`: MIT license.
- `CONTRIBUTING.md`: contribution workflow.
- `CODE_OF_CONDUCT.md`: contributor conduct.
- `CHANGELOG.md`: initial changelog.

---

### Task 1: Package Skeleton

**Files:**
- Create: `pyproject.toml`
- Create: `src/codex_oss_kit/__init__.py`
- Create: `tests/test_package.py`

- [ ] **Step 1: Write the package smoke test**

Create `tests/test_package.py`:

```python
from codex_oss_kit import __version__


def test_version_is_defined():
    assert __version__ == "0.1.0"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_package.py -v`

Expected: FAIL with `ModuleNotFoundError: No module named 'codex_oss_kit'`.

- [ ] **Step 3: Create package metadata**

Create `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "codex-oss-application-kit"
version = "0.1.0"
description = "Prepare truthful Codex for Open Source application drafts from maintainer project data."
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
authors = [
  { name = "Noelyou" }
]
dependencies = [
  "PyYAML>=6.0"
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0"
]

[project.scripts]
codex-oss-kit = "codex_oss_kit.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

Create `src/codex_oss_kit/__init__.py`:

```python
__version__ = "0.1.0"
```

- [ ] **Step 4: Run package smoke test**

Run: `python -m pytest tests/test_package.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add pyproject.toml src/codex_oss_kit/__init__.py tests/test_package.py
git commit -m "feat: add Python package skeleton"
```

---

### Task 2: Data Model and YAML Loader

**Files:**
- Create: `src/codex_oss_kit/model.py`
- Create: `src/codex_oss_kit/loader.py`
- Create: `examples/project.yml`
- Create: `tests/test_loader.py`

- [ ] **Step 1: Write loader tests**

Create `tests/test_loader.py`:

```python
from pathlib import Path

from codex_oss_kit.loader import load_application_profile


def test_load_application_profile_reads_nested_yaml(tmp_path):
    config = tmp_path / "project.yml"
    config.write_text(
        """
maintainer:
  first_name: Noel
  last_name: You
  email: rollingdoormaster@gmail.com
  github_username: Noelyou
project:
  name: codex-oss-application-kit
  repository_url: https://github.com/Noelyou/codex-oss-application-kit
  maintainer_role: primary maintainer
  description: Helps maintainers prepare Codex for Open Source application drafts.
  evidence:
    - Public repository with tests and documentation.
    - Maintainer workflow focused on truthful application preparation.
openai:
  organization_id: org_example
  requested_support:
    - API credits
  api_credit_use:
    - Review pull requests.
    - Draft release notes.
""",
        encoding="utf-8",
    )

    profile = load_application_profile(config)

    assert profile.maintainer.github_username == "Noelyou"
    assert profile.project.name == "codex-oss-application-kit"
    assert profile.openai_organization_id == "org_example"
    assert profile.requested_support == ["API credits"]
```

- [ ] **Step 2: Run loader test to verify it fails**

Run: `python -m pytest tests/test_loader.py -v`

Expected: FAIL with `ModuleNotFoundError` for `codex_oss_kit.loader`.

- [ ] **Step 3: Implement dataclasses**

Create `src/codex_oss_kit/model.py`:

```python
from dataclasses import dataclass, field


@dataclass(frozen=True)
class MaintainerProfile:
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    github_username: str = ""

    @property
    def full_name(self) -> str:
        return " ".join(part for part in [self.first_name, self.last_name] if part).strip()


@dataclass(frozen=True)
class ProjectProfile:
    name: str = ""
    repository_url: str = ""
    maintainer_role: str = ""
    description: str = ""
    evidence: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ApplicationProfile:
    maintainer: MaintainerProfile
    project: ProjectProfile
    openai_organization_id: str = ""
    requested_support: list[str] = field(default_factory=list)
    api_credit_use: list[str] = field(default_factory=list)
```

- [ ] **Step 4: Implement YAML loader**

Create `src/codex_oss_kit/loader.py`:

```python
from pathlib import Path
from typing import Any

import yaml

from codex_oss_kit.model import ApplicationProfile, MaintainerProfile, ProjectProfile


class ConfigError(ValueError):
    """Raised when the project profile cannot be loaded."""


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def load_application_profile(path: str | Path) -> ApplicationProfile:
    config_path = Path(path)
    if not config_path.exists():
        raise ConfigError(f"Config file not found: {config_path}")

    try:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid YAML in {config_path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise ConfigError("Config file must contain a YAML object at the top level.")

    maintainer_raw = raw.get("maintainer") or {}
    project_raw = raw.get("project") or {}
    openai_raw = raw.get("openai") or {}

    return ApplicationProfile(
        maintainer=MaintainerProfile(
            first_name=str(maintainer_raw.get("first_name", "")).strip(),
            last_name=str(maintainer_raw.get("last_name", "")).strip(),
            email=str(maintainer_raw.get("email", "")).strip(),
            github_username=str(maintainer_raw.get("github_username", "")).strip(),
        ),
        project=ProjectProfile(
            name=str(project_raw.get("name", "")).strip(),
            repository_url=str(project_raw.get("repository_url", "")).strip(),
            maintainer_role=str(project_raw.get("maintainer_role", "")).strip(),
            description=str(project_raw.get("description", "")).strip(),
            evidence=_string_list(project_raw.get("evidence")),
        ),
        openai_organization_id=str(openai_raw.get("organization_id", "")).strip(),
        requested_support=_string_list(openai_raw.get("requested_support")),
        api_credit_use=_string_list(openai_raw.get("api_credit_use")),
    )
```

- [ ] **Step 5: Add example config**

Create `examples/project.yml`:

```yaml
maintainer:
  first_name: Noel
  last_name: You
  email: rollingdoormaster@gmail.com
  github_username: Noelyou

project:
  name: codex-oss-application-kit
  repository_url: https://github.com/Noelyou/codex-oss-application-kit
  maintainer_role: primary maintainer
  description: Helps open-source maintainers prepare truthful Codex for Open Source application drafts.
  evidence:
    - Public repository with a tested Python CLI.
    - Documentation for ethical, truthful application preparation.
    - Maintainer workflow for issue triage, release notes, and application evidence collection.

openai:
  organization_id: org_example_replace_me
  requested_support:
    - API credits
    - ChatGPT Pro with Codex
  api_credit_use:
    - Review pull requests and suggest test coverage.
    - Triage issues and draft maintainer responses.
    - Draft release notes and regression checklists.
```

- [ ] **Step 6: Run loader tests**

Run: `python -m pytest tests/test_loader.py -v`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/codex_oss_kit/model.py src/codex_oss_kit/loader.py examples/project.yml tests/test_loader.py
git commit -m "feat: load application profiles from YAML"
```

---

### Task 3: Validation Checks

**Files:**
- Create: `src/codex_oss_kit/checks.py`
- Create: `tests/test_checks.py`

- [ ] **Step 1: Write validation tests**

Create `tests/test_checks.py`:

```python
from codex_oss_kit.checks import run_checks
from codex_oss_kit.model import ApplicationProfile, MaintainerProfile, ProjectProfile


def test_run_checks_reports_missing_required_fields():
    profile = ApplicationProfile(
        maintainer=MaintainerProfile(),
        project=ProjectProfile(),
    )

    result = run_checks(profile)

    messages = [issue.message for issue in result.issues]
    assert "Maintainer first name is missing." in messages
    assert "GitHub repository URL is missing." in messages
    assert "OpenAI organization ID is missing." in messages
    assert result.ok is False


def test_run_checks_accepts_complete_profile():
    profile = ApplicationProfile(
        maintainer=MaintainerProfile(
            first_name="Noel",
            last_name="You",
            email="rollingdoormaster@gmail.com",
            github_username="Noelyou",
        ),
        project=ProjectProfile(
            name="codex-oss-application-kit",
            repository_url="https://github.com/Noelyou/codex-oss-application-kit",
            maintainer_role="primary maintainer",
            description="Maintainer application helper.",
            evidence=["Public repository with tests.", "Documented maintainer workflow."],
        ),
        openai_organization_id="org_example",
        requested_support=["API credits"],
        api_credit_use=["Review pull requests.", "Draft release notes."],
    )

    result = run_checks(profile)

    assert result.ok is True
    assert result.issues == []
```

- [ ] **Step 2: Run validation tests to verify they fail**

Run: `python -m pytest tests/test_checks.py -v`

Expected: FAIL with `ModuleNotFoundError` for `codex_oss_kit.checks`.

- [ ] **Step 3: Implement validation checks**

Create `src/codex_oss_kit/checks.py`:

```python
from dataclasses import dataclass

from codex_oss_kit.model import ApplicationProfile


@dataclass(frozen=True)
class CheckIssue:
    severity: str
    message: str


@dataclass(frozen=True)
class CheckResult:
    issues: list[CheckIssue]

    @property
    def ok(self) -> bool:
        return not any(issue.severity == "error" for issue in self.issues)


def run_checks(profile: ApplicationProfile) -> CheckResult:
    issues: list[CheckIssue] = []

    required = [
        (profile.maintainer.first_name, "Maintainer first name is missing."),
        (profile.maintainer.last_name, "Maintainer last name is missing."),
        (profile.maintainer.email, "Maintainer email is missing."),
        (profile.maintainer.github_username, "GitHub username is missing."),
        (profile.project.name, "Project name is missing."),
        (profile.project.repository_url, "GitHub repository URL is missing."),
        (profile.project.maintainer_role, "Maintainer role is missing."),
        (profile.project.description, "Project description is missing."),
        (profile.openai_organization_id, "OpenAI organization ID is missing."),
    ]

    for value, message in required:
        if not str(value).strip():
            issues.append(CheckIssue("error", message))

    if not profile.project.evidence:
        issues.append(CheckIssue("error", "Project evidence is missing."))
    elif len(profile.project.evidence) < 2:
        issues.append(CheckIssue("warning", "Project evidence is thin; add usage, maintenance, or ecosystem details."))

    if not profile.api_credit_use:
        issues.append(CheckIssue("error", "Planned API credit use is missing."))

    if not profile.requested_support:
        issues.append(CheckIssue("warning", "Requested support is empty; select at least API credits if applicable."))

    return CheckResult(issues)
```

- [ ] **Step 4: Run validation tests**

Run: `python -m pytest tests/test_checks.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/codex_oss_kit/checks.py tests/test_checks.py
git commit -m "feat: validate application profile completeness"
```

---

### Task 4: Markdown Renderer

**Files:**
- Create: `src/codex_oss_kit/render.py`
- Create: `tests/test_render.py`

- [ ] **Step 1: Write renderer test**

Create `tests/test_render.py`:

```python
from codex_oss_kit.model import ApplicationProfile, MaintainerProfile, ProjectProfile
from codex_oss_kit.render import render_application


def test_render_application_includes_form_answers():
    profile = ApplicationProfile(
        maintainer=MaintainerProfile(
            first_name="Noel",
            last_name="You",
            email="rollingdoormaster@gmail.com",
            github_username="Noelyou",
        ),
        project=ProjectProfile(
            name="codex-oss-application-kit",
            repository_url="https://github.com/Noelyou/codex-oss-application-kit",
            maintainer_role="primary maintainer",
            description="Helps maintainers prepare truthful application drafts.",
            evidence=["Public tested CLI.", "Open-source maintenance workflow."],
        ),
        openai_organization_id="org_example",
        requested_support=["API credits"],
        api_credit_use=["Review pull requests.", "Draft release notes."],
    )

    output = render_application(profile)

    assert "# Codex for Open Source Application Draft" in output
    assert "GitHub username: Noelyou" in output
    assert "https://github.com/Noelyou/codex-oss-application-kit" in output
    assert "We will use API credits for Codex-assisted maintainer workflows" in output
```

- [ ] **Step 2: Run renderer test to verify it fails**

Run: `python -m pytest tests/test_render.py -v`

Expected: FAIL with `ModuleNotFoundError` for `codex_oss_kit.render`.

- [ ] **Step 3: Implement renderer**

Create `src/codex_oss_kit/render.py`:

```python
from codex_oss_kit.model import ApplicationProfile


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_application(profile: ApplicationProfile) -> str:
    evidence_text = " ".join(profile.project.evidence)
    api_use_text = " ".join(profile.api_credit_use)
    requested = ", ".join(profile.requested_support) if profile.requested_support else "Not specified"

    qualify_answer = (
        f"I am a {profile.project.maintainer_role} of {profile.project.name}, "
        f"an active open-source project. {profile.project.description} "
        f"Relevant evidence: {evidence_text} "
        "Codex support would help maintain the project through faster review, triage, "
        "release preparation, and quality improvements for downstream users."
    )

    api_answer = (
        "We will use API credits for Codex-assisted maintainer workflows: "
        f"{api_use_text} "
        "The credits will be used only for core open-source project work."
    )

    return f"""# Codex for Open Source Application Draft

Official form: https://openai.com/form/codex-for-oss/

## Applicant

- First name: {profile.maintainer.first_name}
- Last name: {profile.maintainer.last_name}
- Email: {profile.maintainer.email}
- GitHub username: {profile.maintainer.github_username}

## Project

- Repository: {profile.project.repository_url}
- Role: {profile.project.maintainer_role}
- Requested support: {requested}
- OpenAI organization ID: {profile.openai_organization_id}

## Why does this repository qualify?

{qualify_answer}

## How will you use API credits?

{api_answer}

## Evidence

{_bullets(profile.project.evidence)}
"""
```

- [ ] **Step 4: Run renderer test**

Run: `python -m pytest tests/test_render.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/codex_oss_kit/render.py tests/test_render.py
git commit -m "feat: render application drafts"
```

---

### Task 5: Command-Line Interface

**Files:**
- Create: `src/codex_oss_kit/cli.py`
- Create: `tests/test_cli.py`

- [ ] **Step 1: Write CLI tests**

Create `tests/test_cli.py`:

```python
from codex_oss_kit.cli import main


VALID_CONFIG = """
maintainer:
  first_name: Noel
  last_name: You
  email: rollingdoormaster@gmail.com
  github_username: Noelyou
project:
  name: codex-oss-application-kit
  repository_url: https://github.com/Noelyou/codex-oss-application-kit
  maintainer_role: primary maintainer
  description: Helps maintainers prepare truthful application drafts.
  evidence:
    - Public tested CLI.
    - Open-source maintenance workflow.
openai:
  organization_id: org_example
  requested_support:
    - API credits
  api_credit_use:
    - Review pull requests.
    - Draft release notes.
"""


def test_cli_render_outputs_application(tmp_path, capsys):
    config = tmp_path / "project.yml"
    config.write_text(VALID_CONFIG, encoding="utf-8")

    exit_code = main(["render", str(config)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "# Codex for Open Source Application Draft" in captured.out
    assert captured.err == ""


def test_cli_check_returns_nonzero_for_missing_fields(tmp_path, capsys):
    config = tmp_path / "project.yml"
    config.write_text("maintainer: {}\nproject: {}\nopenai: {}\n", encoding="utf-8")

    exit_code = main(["check", str(config)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "ERROR: Maintainer first name is missing." in captured.out
```

- [ ] **Step 2: Run CLI tests to verify they fail**

Run: `python -m pytest tests/test_cli.py -v`

Expected: FAIL with `ModuleNotFoundError` for `codex_oss_kit.cli`.

- [ ] **Step 3: Implement CLI**

Create `src/codex_oss_kit/cli.py`:

```python
import argparse
import sys

from codex_oss_kit.checks import run_checks
from codex_oss_kit.loader import ConfigError, load_application_profile
from codex_oss_kit.render import render_application


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="codex-oss-kit",
        description="Prepare truthful Codex for Open Source application drafts.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    render_parser = subparsers.add_parser("render", help="Render a Markdown application draft.")
    render_parser.add_argument("config", help="Path to a YAML project profile.")

    check_parser = subparsers.add_parser("check", help="Check a YAML project profile for missing data.")
    check_parser.add_argument("config", help="Path to a YAML project profile.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        profile = load_application_profile(args.config)
    except ConfigError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.command == "render":
        print(render_application(profile))
        return 0

    if args.command == "check":
        result = run_checks(profile)
        if not result.issues:
            print("OK: application profile is complete.")
            return 0
        for issue in result.issues:
            print(f"{issue.severity.upper()}: {issue.message}")
        return 0 if result.ok else 1

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run CLI tests**

Run: `python -m pytest tests/test_cli.py -v`

Expected: PASS.

- [ ] **Step 5: Run full test suite**

Run: `python -m pytest -v`

Expected: PASS for all tests.

- [ ] **Step 6: Commit**

```bash
git add src/codex_oss_kit/cli.py tests/test_cli.py
git commit -m "feat: add render and check CLI commands"
```

---

### Task 6: Open-Source Documentation

**Files:**
- Create: `README.md`
- Create: `LICENSE`
- Create: `CONTRIBUTING.md`
- Create: `CODE_OF_CONDUCT.md`
- Create: `CHANGELOG.md`
- Modify: `CODEX_OSS_APPLICATION.md`

- [ ] **Step 1: Create README**

Create `README.md`:

```markdown
# codex-oss-application-kit

Prepare truthful Codex for Open Source application drafts from maintainer project data.

This project helps open-source maintainers collect the information needed for the Codex for Open Source application, check for missing fields, and render a Markdown draft that can be reviewed before using the official OpenAI form.

It does not guarantee acceptance, fabricate project metrics, or submit the form automatically.

## Quick Start

```powershell
python -m pip install -e ".[dev]"
codex-oss-kit check examples/project.yml
codex-oss-kit render examples/project.yml
```

## Example Config

```yaml
maintainer:
  first_name: Noel
  last_name: You
  email: rollingdoormaster@gmail.com
  github_username: Noelyou

project:
  name: codex-oss-application-kit
  repository_url: https://github.com/Noelyou/codex-oss-application-kit
  maintainer_role: primary maintainer
  description: Helps open-source maintainers prepare truthful Codex for Open Source application drafts.
  evidence:
    - Public repository with a tested Python CLI.
    - Documentation for ethical, truthful application preparation.

openai:
  organization_id: org_example_replace_me
  requested_support:
    - API credits
  api_credit_use:
    - Review pull requests and suggest test coverage.
    - Triage issues and draft maintainer responses.
```

## Commands

`codex-oss-kit check <config>` reports missing required fields and evidence warnings.

`codex-oss-kit render <config>` prints a Markdown application draft.

## Ethical Use

Use real project data. Do not claim adoption, usage, maintainer status, or ecosystem importance that you cannot support with evidence.

## Development

```powershell
python -m pip install -e ".[dev]"
python -m pytest -v
```
```

- [ ] **Step 2: Create MIT license**

Create `LICENSE` using the standard MIT license text with copyright:

```text
MIT License

Copyright (c) 2026 Noelyou

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 3: Create contributing guide**

Create `CONTRIBUTING.md`:

```markdown
# Contributing

Thanks for considering a contribution.

## Local Setup

```powershell
python -m pip install -e ".[dev]"
python -m pytest -v
```

## Pull Requests

- Keep changes focused.
- Add or update tests for behavior changes.
- Keep application guidance truthful and evidence-based.
- Do not add automation that submits forms or fabricates project metrics.
```

- [ ] **Step 4: Create code of conduct**

Create `CODE_OF_CONDUCT.md`:

```markdown
# Code of Conduct

This project expects respectful, constructive participation.

Do not harass, threaten, insult, or abuse other contributors. Keep discussion focused on the project and its users.

Maintainers may remove comments, issues, or pull requests that violate these expectations.
```

- [ ] **Step 5: Create changelog**

Create `CHANGELOG.md`:

```markdown
# Changelog

## 0.1.0 - 2026-06-01

- Add initial Python CLI project.
- Add YAML application profile loading.
- Add profile completeness checks.
- Add Markdown application draft rendering.
- Add open-source project documentation.
```

- [ ] **Step 6: Update application worksheet**

Modify `CODEX_OSS_APPLICATION.md` status to say:

```markdown
Status: project is being built locally; GitHub publication and real public repository URL are still required before submission.
```

- [ ] **Step 7: Run full test suite**

Run: `python -m pytest -v`

Expected: PASS for all tests.

- [ ] **Step 8: Commit**

```bash
git add README.md LICENSE CONTRIBUTING.md CODE_OF_CONDUCT.md CHANGELOG.md CODEX_OSS_APPLICATION.md
git commit -m "docs: add open-source project documentation"
```

---

### Task 7: Final Local Verification

**Files:**
- Modify only if verification exposes a defect.

- [ ] **Step 1: Install project in editable mode**

Run: `python -m pip install -e ".[dev]"`

Expected: package installs successfully.

- [ ] **Step 2: Run tests**

Run: `python -m pytest -v`

Expected: all tests pass.

- [ ] **Step 3: Run profile check**

Run: `codex-oss-kit check examples/project.yml`

Expected: output includes warnings or errors only for intentionally replaceable example values if those are not accepted by validation. If validation treats the example as complete, output is `OK: application profile is complete.`

- [ ] **Step 4: Render application draft**

Run: `codex-oss-kit render examples/project.yml`

Expected: output starts with `# Codex for Open Source Application Draft` and includes the repository URL.

- [ ] **Step 5: Inspect git status**

Run: `git status --short`

Expected: no unstaged implementation changes, except any files intentionally left uncommitted for publication setup.

---

### Task 8: GitHub Publication Preparation

**Files:**
- Modify: `CODEX_OSS_APPLICATION.md`

- [ ] **Step 1: Create public GitHub repository**

Use GitHub UI or `gh` if authenticated to create `Noelyou/codex-oss-application-kit` as a public repository.

Expected: repository URL is `https://github.com/Noelyou/codex-oss-application-kit`.

- [ ] **Step 2: Add remote**

Run: `git remote add origin https://github.com/Noelyou/codex-oss-application-kit.git`

Expected: `git remote -v` shows `origin`.

- [ ] **Step 3: Push repository**

Run: `git push -u origin master`

Expected: push succeeds and GitHub shows project files publicly.

- [ ] **Step 4: Create first maintenance issue**

Create an issue titled:

```text
Add optional public GitHub metadata checks
```

Issue body:

```markdown
The first release is intentionally offline-only. A useful next step is an optional check that reads public GitHub repository metadata without authentication and reports stars, forks, open issues, and last push time as maintainer evidence.

This should remain optional and should not be used to fabricate qualification claims.
```

- [ ] **Step 5: Update application worksheet**

Modify `CODEX_OSS_APPLICATION.md` with:

```markdown
| GitHub repository URL | https://github.com/Noelyou/codex-oss-application-kit |
```

Set status to:

```markdown
Status: public repository created; application still needs real OpenAI Organization ID and final user review before submission.
```

- [ ] **Step 6: Commit worksheet update**

```bash
git add CODEX_OSS_APPLICATION.md
git commit -m "docs: update Codex OSS application repository URL"
git push
```

---

## Self-Review

Spec coverage:

- Python CLI with `render` and `check`: covered by Tasks 1 through 5.
- Typed data model: covered by Task 2.
- YAML examples: covered by Task 2.
- Markdown rendering: covered by Task 4.
- Required field validation: covered by Task 3.
- Unit and CLI tests: covered by Tasks 1 through 5 and Task 7.
- Open-source files: covered by Task 6.
- Public GitHub publication and first issue: covered by Task 8.
- Honest application language: covered by README, renderer, and worksheet updates.

Placeholder scan: no unfinished task markers or incomplete task instructions are intentionally left in this plan. The only replaceable values are explicit example values such as `org_example_replace_me`, which are part of sample user data and not unfinished plan work.

Type consistency: modules use `ApplicationProfile`, `MaintainerProfile`, `ProjectProfile`, `ConfigError`, `run_checks`, and `render_application` consistently across tasks.
