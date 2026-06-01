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
        issues.append(
            CheckIssue(
                "warning",
                "Project evidence is thin; add usage, maintenance, or ecosystem details.",
            )
        )

    if not profile.api_credit_use:
        issues.append(CheckIssue("error", "Planned API credit use is missing."))

    if not profile.requested_support:
        issues.append(
            CheckIssue(
                "warning",
                "Requested support is empty; select at least API credits if applicable.",
            )
        )

    return CheckResult(issues)
