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
