import argparse
import sys

from codex_oss_kit.checks import run_checks
from codex_oss_kit.loader import ConfigError, load_application_profile
from codex_oss_kit.render import render_application


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="codex-oss-kit",
        description="Prepare Codex for Open Source application drafts.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    render_parser = subparsers.add_parser(
        "render",
        help="Render an application draft from a project profile.",
    )
    render_parser.add_argument("config", help="Path to the project YAML profile.")

    check_parser = subparsers.add_parser(
        "check",
        help="Check a project profile for missing application fields.",
    )
    check_parser.add_argument("config", help="Path to the project YAML profile.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    try:
        profile = load_application_profile(args.config)
    except ConfigError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.command == "render":
        print(render_application(profile))
        return 0

    result = run_checks(profile)
    for issue in result.issues:
        print(f"{issue.severity.upper()}: {issue.message}")

    if result.ok:
        print("OK: application profile is complete.")

    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
