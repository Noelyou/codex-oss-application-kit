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
