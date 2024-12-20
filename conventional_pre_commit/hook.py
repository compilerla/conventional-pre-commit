import argparse
import sys

from conventional_pre_commit import output
from conventional_pre_commit.format import ConventionalCommit

RESULT_SUCCESS = 0
RESULT_FAIL = 1


def main(argv=[]):
    parser = argparse.ArgumentParser(
        prog="conventional-pre-commit", description="Check a git commit message for Conventional Commits formatting."
    )
    parser.add_argument(
        "types", type=str, nargs="*", default=ConventionalCommit.DEFAULT_TYPES, help="Optional list of types to support"
    )
    parser.add_argument("input", type=str, help="A file containing a git commit message")
    parser.add_argument("--no-color", action="store_false", default=True, dest="color", help="Disable color in output.")
    parser.add_argument(
        "--force-scope", action="store_false", default=True, dest="optional_scope", help="Force commit to have scope defined."
    )
    parser.add_argument(
        "--scopes",
        type=str,
        default=None,
        help="List of scopes to support. Scopes should be separated by commas with no spaces (e.g. api,client).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Force commit to strictly follow Conventional Commits formatting. Disallows fixup! and merge commits.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        dest="verbose",
        default=False,
        help="Print more verbose error output.",
    )

    if len(argv) < 1:
        argv = sys.argv[1:]

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return RESULT_FAIL

    try:
        with open(args.input, encoding="utf-8") as f:
            commit_msg = f.read()
    except UnicodeDecodeError:
        print(output.unicode_decode_error(args.color))
        return RESULT_FAIL
    if args.scopes:
        scopes = args.scopes.split(",")
    else:
        scopes = args.scopes

    commit = ConventionalCommit(commit_msg, args.types, args.optional_scope, scopes)

    if not args.strict:
        if commit.has_autosquash_prefix():
            return RESULT_SUCCESS
        if commit.is_merge():
            return RESULT_SUCCESS

    if commit.is_valid():
        return RESULT_SUCCESS

    print(output.fail(commit, use_color=args.color))

    if not args.verbose:
        print(output.verbose_arg(use_color=args.color))
    else:
        print(output.fail_verbose(commit, use_color=args.color))

    return RESULT_FAIL


if __name__ == "__main__":
    raise SystemExit(main())
