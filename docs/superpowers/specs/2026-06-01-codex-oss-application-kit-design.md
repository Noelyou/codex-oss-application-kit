# codex-oss-application-kit Design

Date: 2026-06-01

## Goal

Create a real open-source project that helps maintainers prepare honest, complete Codex for Open Source application materials. The project should be useful on its own, maintainable over time, and suitable for publication as a public GitHub repository.

The tool will not guarantee acceptance, fabricate usage metrics, or automate submission to OpenAI. It will help maintainers organize evidence, identify missing data, and generate paste-ready application drafts.

## Users

Primary users are open-source maintainers who want to apply for Codex for Open Source and need a repeatable way to collect project evidence, draft application answers, and check for missing fields.

Secondary users are maintainers who want a general checklist for documenting project health, maintenance activity, and API credit use cases.

## First Release Scope

The first release is a Python CLI named `codex-oss-kit`.

Commands:

- `codex-oss-kit render <config>` generates a Markdown application draft from a YAML project file.
- `codex-oss-kit check <config>` validates required fields and reports missing or weak evidence.

The release includes:

- A typed internal data model for application fields.
- YAML input examples.
- Markdown output rendering.
- Basic validation for required fields.
- Unit tests for loading, validation, and rendering.
- Open-source project files: `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `CHANGELOG.md`.

Out of scope for the first release:

- Submitting the OpenAI form automatically.
- Claiming a project qualifies without maintainer-provided evidence.
- Authenticated GitHub integration.
- Package publishing to PyPI.

## Architecture

The project uses a standard Python `src/` layout:

- `src/codex_oss_kit/cli.py`: command-line entry point and argument parsing.
- `src/codex_oss_kit/model.py`: dataclasses for project and application data.
- `src/codex_oss_kit/loader.py`: YAML loading and normalization.
- `src/codex_oss_kit/render.py`: Markdown draft generation.
- `src/codex_oss_kit/checks.py`: validation and evidence checks.
- `tests/`: focused pytest coverage.
- `examples/project.yml`: realistic example input.

The CLI depends on small, common packages only. `PyYAML` is acceptable for YAML parsing; the rest should use the Python standard library where practical.

## Data Flow

1. User creates or edits a YAML project profile.
2. `loader.py` parses YAML into plain dictionaries.
3. `model.py` normalizes values into typed objects.
4. `checks.py` reports missing required fields and weak evidence.
5. `render.py` generates a Markdown application draft.
6. The maintainer manually reviews the output and pastes appropriate text into the official OpenAI form.

## Validation

The checker should report:

- Missing maintainer name.
- Missing email.
- Missing GitHub username.
- Missing public repository URL.
- Missing maintainer role.
- Missing OpenAI organization ID.
- Missing project evidence.
- Missing planned API credit use.

Warnings should be clear and actionable. The tool should distinguish between hard missing fields and softer evidence warnings.

## Error Handling

Invalid config files should return a non-zero exit code with a concise message. The tool should avoid tracebacks for expected user errors such as missing files, malformed YAML, or missing required fields.

Unexpected exceptions can still surface during development, but command handlers should keep common user mistakes readable.

## Testing

The first release should include tests for:

- Loading a valid YAML file.
- Reporting missing required fields.
- Rendering application draft text.
- CLI success path for `render`.
- CLI non-zero behavior for invalid input.

Tests should run with `python -m pytest`.

## Documentation

The README should explain:

- What the tool does.
- What it does not do.
- Quick start commands.
- Example YAML.
- Example output.
- How to contribute.
- Ethical use: users must provide real project data and submit truthful applications.

The repository should include a permissive open-source license. MIT is a reasonable default.

## Release and Maintenance Plan

Initial public release:

1. Build the first CLI and tests locally.
2. Create an initial commit history with project files.
3. Publish the repository publicly on GitHub.
4. Add project topics and a concise repository description.
5. Open at least one issue for planned improvements, such as optional unauthenticated GitHub metadata checks.

Maintenance after release:

- Review issues and pull requests.
- Keep templates aligned with the current official OpenAI form.
- Add GitHub metadata checks only after the core offline workflow is stable.

## Application Use

After the project is published, the Codex for Open Source application should describe the repository honestly as a new open-source maintainer tool. The application should not overstate adoption. It can emphasize the project's purpose, public availability, maintainability, tests, documentation, and planned maintainer workflows.

