from codex_oss_kit.model import ApplicationProfile


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def render_application(profile: ApplicationProfile) -> str:
    evidence_text = " ".join(profile.project.evidence)
    api_use_text = " ".join(profile.api_credit_use)
    requested = (
        ", ".join(profile.requested_support)
        if profile.requested_support
        else "Not specified"
    )

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
