# Codex for Open Source Application

Apply here: https://openai.com/form/codex-for-oss/

Official program page: https://developers.openai.com/community/codex-for-oss

Status: public GitHub repository has been created and pushed to `main`; final submission still requires first name, last name, OpenAI Organization ID, and final user review.

## Confirmed So Far

- GitHub username: Noelyou
- ChatGPT/OpenAI email candidate: rollingdoormaster@gmail.com
- Local git remote: https://github.com/Noelyou/codex-oss-application-kit.git
- Public repository URL: https://github.com/Noelyou/codex-oss-application-kit
- Local implementation branch: codex/oss-application-kit
- Published main commit: 2cfc9b59d8bd55995710b5f6f5fa86c7ad6174b6
- Local tests: `python -m pytest -v` passed with 14 tests
- GitHub connector status: unavailable due to revoked OAuth token
- Remote push status: verified with `git ls-remote --heads origin`

## Official Eligibility Notes

- Maintainers of active open-source projects can apply.
- OpenAI looks for repository usage, ecosystem importance, and evidence of active maintenance.
- Relevant maintenance work includes pull request review, issue triage, release management, security, and code quality.
- Selected maintainers may receive six months of ChatGPT Pro with Codex, API credits, and possible conditional Codex Security access.
- Applications are reviewed on a rolling basis, and selected applicants are notified by email.

## Form Fields

| Field | Suggested value |
| --- | --- |
| First name | TODO |
| Last name | TODO |
| Email | rollingdoormaster@gmail.com |
| GitHub username | Noelyou |
| GitHub repository URL | https://github.com/Noelyou/codex-oss-application-kit |
| Role | Primary maintainer |
| Why does this repository qualify? | Use the draft below |
| Interested in | Select API credits for my project; optionally select Codex Security if you want security review help |
| OpenAI Organization ID | TODO: find it at https://platform.openai.com/ |
| How will you use API credits? | Use the draft below |
| Anything else? | Use the optional draft below or leave blank |

## Paste-Ready Drafts

### Why does this repository qualify?

Use this draft for the official form.

```text
I am the primary maintainer of codex-oss-application-kit, a public open-source Python CLI that helps maintainers prepare truthful Codex for Open Source application drafts from structured project data. The repository includes a tested CLI, YAML profile loading, completeness checks, Markdown rendering, examples, and open-source contribution documentation. Codex support would help maintain issue triage, pull request review, release preparation, tests, and template updates as the official application process changes.
```

Shorter conservative version:

```text
I am the primary maintainer of codex-oss-application-kit, a new public open-source Python CLI for maintainers preparing truthful Codex for Open Source application drafts. It includes tests, examples, documentation, and a maintainer workflow focused on issue triage, PR review, release notes, and keeping application templates aligned with the official process.
```

### How will you use API credits for your project?

```text
We will use API credits for Codex-assisted maintainer workflows: reviewing pull requests, triaging issues, drafting fixes and tests, improving release notes, checking regressions before releases, and automating repetitive maintenance tasks. The credits will be used only for core open-source project work.
```

### Anything else we should know?

```text
I can provide additional evidence of maintainer access, release history, issue triage, pull request reviews, or project adoption if needed. The goal is to use Codex to reduce maintenance backlog and improve reliability for the project and its downstream users.
```

## Pre-Submission Checklist

- [ ] GitHub profile is public.
- [ ] Target GitHub repository is public.
- [ ] Repository URL is correct.
- [ ] Role is accurate: Primary maintainer or Core maintainer.
- [ ] Qualification text includes real metrics or ecosystem importance.
- [ ] OpenAI Organization ID is filled in.
- [ ] Email matches the ChatGPT account that should receive Pro access.
- [ ] Form terms are reviewed before submission.

## Missing Information

1. First name
2. Last name
3. OpenAI Organization ID
4. Whether to request Codex Security in addition to API credits

## Current Blocker

The Codex for Open Source form requires a public GitHub repository with verifiable project files. The repository URL exists and the `main` branch has been pushed and verified. Final submission still requires user-specific identity and OpenAI organization fields.

## Best Next Action

Fill in your first name, last name, and OpenAI Organization ID before submitting the official form. If you want issue-maintenance evidence before submitting, create the planned first issue listed below.

## Planned First Issue

Title:

```text
Add optional public GitHub metadata checks
```

Body:

```text
The first release is intentionally offline-only. A useful next step is an optional check that reads public GitHub repository metadata without authentication and reports stars, forks, open issues, and last push time as maintainer evidence.

This should remain optional and should not be used to fabricate qualification claims.
```
