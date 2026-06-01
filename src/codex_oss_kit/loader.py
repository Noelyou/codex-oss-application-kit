from collections.abc import Mapping
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


def _section(raw: dict[str, Any], name: str) -> Mapping[str, Any]:
    value = raw.get(name)
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ConfigError(f"{name} section must be a YAML object.")
    return value


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

    maintainer_raw = _section(raw, "maintainer")
    project_raw = _section(raw, "project")
    openai_raw = _section(raw, "openai")

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
