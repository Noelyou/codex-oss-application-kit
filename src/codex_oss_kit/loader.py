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
        return [_optional_string(item) for item in value if _optional_string(item)]
    text = _optional_string(value)
    return [text] if text else []


def _optional_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


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
        text = config_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ConfigError(f"Could not read config file {config_path}: {exc}") from exc

    try:
        raw = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid YAML in {config_path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise ConfigError("Config file must contain a YAML object at the top level.")

    maintainer_raw = _section(raw, "maintainer")
    project_raw = _section(raw, "project")
    openai_raw = _section(raw, "openai")

    return ApplicationProfile(
        maintainer=MaintainerProfile(
            first_name=_optional_string(maintainer_raw.get("first_name")),
            last_name=_optional_string(maintainer_raw.get("last_name")),
            email=_optional_string(maintainer_raw.get("email")),
            github_username=_optional_string(maintainer_raw.get("github_username")),
        ),
        project=ProjectProfile(
            name=_optional_string(project_raw.get("name")),
            repository_url=_optional_string(project_raw.get("repository_url")),
            maintainer_role=_optional_string(project_raw.get("maintainer_role")),
            description=_optional_string(project_raw.get("description")),
            evidence=_string_list(project_raw.get("evidence")),
        ),
        openai_organization_id=_optional_string(openai_raw.get("organization_id")),
        requested_support=_string_list(openai_raw.get("requested_support")),
        api_credit_use=_string_list(openai_raw.get("api_credit_use")),
    )
