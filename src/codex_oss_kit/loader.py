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
