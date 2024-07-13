import argparse
import sys

from conventional_pre_commit import format

RESULT_SUCCESS = 0
RESULT_FAIL = 1


class Colors:
    LBLUE = "\033[00;34m"
    LRED = "\033[01;31m"
    RESTORE = "\033[0m"
    YELLOW = "\033[00;33m"


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
    parser.add_argument(
        "--skip-merge-commits",
        action="store_true",
        dest="skip_merge_commits",
        help="Do not check format for merge commits.",
    )

    if len(argv) < 1:
        argv = sys.argv[1:]

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return RESULT_FAIL

    try:
        with open(args.input, encoding="utf-8") as f:
            message = f.read()
    except UnicodeDecodeError:
        print(
            f"""
{Colors.LRED}[Bad Commit message encoding] {Colors.RESTORE}

{Colors.YELLOW}conventional-pre-commit couldn't decode your commit message.{Colors.RESTORE}
{Colors.YELLOW}UTF-8{Colors.RESTORE} encoding is assumed, please configure git to write commit messages in UTF-8.
See {Colors.LBLUE}https://git-scm.com/docs/git-commit/#_discussion{Colors.RESTORE} for more.
        """
        )
        return RESULT_FAIL
    if args.scopes:
        scopes = args.scopes.split(",")
    else:
        scopes = args.scopes

    if args.skip_merge_commits:
        if format.is_merge_commit(message):
            return RESULT_SUCCESS

    if not args.strict:
        if format.has_autosquash_prefix(message):
            return RESULT_SUCCESS

    if format.is_conventional(message, args.types, args.optional_scope, scopes):
        return RESULT_SUCCESS
    else:
        print(
            f"""
        {Colors.LRED}[Bad Commit message] >>{Colors.RESTORE} {message}
        {Colors.YELLOW}Your commit message does not follow Conventional Commits formatting
        {Colors.LBLUE}https://www.conventionalcommits.org/{Colors.YELLOW}

        Conventional Commits start with one of the below types, followed by a colon,
        followed by the commit subject and an optional body seperated by a blank line:{Colors.RESTORE}

            {" ".join(format.conventional_types(args.types))}

        {Colors.YELLOW}Example commit message adding a feature:{Colors.RESTORE}

            feat: implement new API

        {Colors.YELLOW}Example commit message fixing an issue:{Colors.RESTORE}

            fix: remove infinite loop

        {Colors.YELLOW}Example commit with scope in parentheses after the type for more context:{Colors.RESTORE}

            fix(account): remove infinite loop

        {Colors.YELLOW}Example commit with a body:{Colors.RESTORE}

            fix: remove infinite loop

            Additional information on the issue caused by the infinite loop
            """
        )
        return RESULT_FAIL


if __name__ == "__main__":
    raise SystemExit(main())
