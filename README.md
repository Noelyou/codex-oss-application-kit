# codex-oss-application-kit

Prepare truthful Codex for Open Source application drafts from maintainer project data.

This project helps open-source maintainers collect the information needed for the Codex for Open Source application, check for missing fields, and render a Markdown draft that can be reviewed before using the official OpenAI form.

It does not guarantee acceptance, fabricate project metrics, submit the form automatically, or replace the official application process.

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

## Commands

`codex-oss-kit check <config>` loads a YAML project profile, reports missing required application fields, and warns when evidence or requested support is thin. It exits with `0` when there are no errors and `1` when required data is missing.

`codex-oss-kit render <config>` loads a YAML project profile and prints a Markdown application draft to standard output.

Both commands return `2` when the config file cannot be read or parsed.

## Ethical Use

Use real project data. Do not claim adoption, usage, maintainer status, security relevance, or ecosystem importance that you cannot support with evidence.

This tool is for preparation and review. It should not be extended to automate official form submission, invent metrics, or obscure uncertainty in an application.

## Development

```powershell
python -m pip install -e ".[dev]"
python -m pytest -v
```
