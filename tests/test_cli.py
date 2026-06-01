from codex_oss_kit.cli import main


VALID_CONFIG = """
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
"""


def test_cli_render_outputs_application(tmp_path, capsys):
    config = tmp_path / "project.yml"
    config.write_text(VALID_CONFIG, encoding="utf-8")

    exit_code = main(["render", str(config)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "# Codex for Open Source Application Draft" in captured.out
    assert captured.err == ""


def test_cli_check_returns_nonzero_for_missing_fields(tmp_path, capsys):
    config = tmp_path / "project.yml"
    config.write_text(
        """
maintainer: {}
project: {}
openai: {}
""",
        encoding="utf-8",
    )

    exit_code = main(["check", str(config)])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "ERROR: Maintainer first name is missing." in captured.out


def test_cli_check_reports_success_for_complete_profile(tmp_path, capsys):
    config = tmp_path / "project.yml"
    config.write_text(VALID_CONFIG, encoding="utf-8")

    exit_code = main(["check", str(config)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "OK: application profile is complete." in captured.out
    assert captured.err == ""
