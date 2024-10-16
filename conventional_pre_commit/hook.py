import argparse
import sys

from conventional_pre_commit import format, output

RESULT_SUCCESS = 0
RESULT_FAIL = 1


def main(argv=[]):
    parser = argparse.ArgumentParser(
        prog="conventional-pre-commit", description="Check a git commit message for Conventional Commits formatting."
    )
    parser.add_argument("types", type=str, nargs="*", default=format.DEFAULT_TYPES, help="Optional list of types to support")
    parser.add_argument("input", type=str, help="A file containing a git commit message")
    parser.add_argument(
        "--force-scope", action="store_false", default=True, dest="optional_scope", help="Force commit to have scope defined."
    )
    parser.add_argument(
        "--scopes",
        type=str,
        default=None,
        help="Optional list of scopes to support. Scopes should be separated by commas with no spaces (e.g. api,client)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Force commit to strictly follow Conventional Commits formatting. Disallows fixup! style commits.",
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
        print(output.unicode_decode_error())
        return RESULT_FAIL
    if args.scopes:
        scopes = args.scopes.split(",")
    else:
        scopes = args.scopes

    if not args.strict:
        if format.has_autosquash_prefix(commit_msg):
            return RESULT_SUCCESS

    if format.is_conventional(commit_msg, args.types, args.optional_scope, scopes):
        return RESULT_SUCCESS
    else:
        print(output.fail(commit_msg))

    return RESULT_FAIL


if __name__ == "__main__":
    raise SystemExit(main())
