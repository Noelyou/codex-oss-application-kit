from pathlib import Path

import pytest

from codex_oss_kit.loader import ConfigError, load_application_profile


def test_load_application_profile_reads_nested_yaml(tmp_path):
    config = tmp_path / "project.yml"
    config.write_text(
        """
maintainer:
  first_name: Noel
  last_name: You
  email: rollingdoormaster@gmail.com
  github_username: Noelyou
project:
  name: codex-oss-application-kit
  repository_url: https://github.com/Noelyou/codex-oss-application-kit
  maintainer_role: primary maintainer
  description: Helps maintainers prepare Codex for Open Source application drafts.
  evidence:
    - Public repository with tests and documentation.
    - Maintainer workflow focused on truthful application preparation.
openai:
  organization_id: org_example
  requested_support:
    - API credits
  api_credit_use:
    - Review pull requests.
    - Draft release notes.
""",
        encoding="utf-8",
    )

    profile = load_application_profile(config)

    assert profile.maintainer.github_username == "Noelyou"
    assert profile.project.name == "codex-oss-application-kit"
    assert profile.openai_organization_id == "org_example"
    assert profile.requested_support == ["API credits"]


def test_load_application_profile_treats_null_scalars_as_empty_strings(tmp_path):
    config = tmp_path / "project.yml"
    config.write_text(
        """
maintainer:
  first_name:
  last_name: You
project:
  name: codex-oss-application-kit
openai: {}
""",
        encoding="utf-8",
    )

    profile = load_application_profile(config)

    assert profile.maintainer.first_name == ""
    assert profile.maintainer.full_name == "You"


def test_load_application_profile_ignores_null_list_items(tmp_path):
    config = tmp_path / "project.yml"
    config.write_text(
        """
maintainer: {}
project:
  evidence:
    - Public repository with tests.
    -
    - Maintainer workflow focused on truthful application preparation.
openai: {}
""",
        encoding="utf-8",
    )

    profile = load_application_profile(config)

    assert profile.project.evidence == [
        "Public repository with tests.",
        "Maintainer workflow focused on truthful application preparation.",
    ]
    assert "None" not in profile.project.evidence


def test_load_application_profile_wraps_invalid_utf8_as_config_error(tmp_path):
    config = tmp_path / "project.yml"
    config.write_bytes(b"\xff\xfe\xfa")

    with pytest.raises(ConfigError, match="Could not read config file"):
        load_application_profile(config)


@pytest.mark.parametrize("section_name", ["maintainer", "project", "openai"])
def test_load_application_profile_rejects_non_object_nested_sections(
    tmp_path, section_name
):
    config = tmp_path / "project.yml"
    config.write_text(f"{section_name}: nope\n", encoding="utf-8")

    with pytest.raises(
        ConfigError, match=f"{section_name} section must be a YAML object"
    ):
        load_application_profile(config)
