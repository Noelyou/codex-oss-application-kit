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

    rendered = render_application(profile)

    assert "# Codex for Open Source Application Draft" in rendered
    assert "GitHub username: Noelyou" in rendered
    assert (
        "https://github.com/Noelyou/codex-oss-application-kit"
        in rendered
    )
    assert (
        "We will use API credits for Codex-assisted maintainer workflows"
        in rendered
    )
    assert "an active open-source project" not in rendered
    assert "downstream users" not in rendered
