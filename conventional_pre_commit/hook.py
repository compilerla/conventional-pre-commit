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
    parser.add_argument("--encoding", type=str, default=None, help="Optional encoding to use when reading the commit message")
    parser.add_argument("types", type=str, nargs="*", default=format.DEFAULT_TYPES, help="Optional list of types to support")
    parser.add_argument("input", type=str, help="A file containing a git commit message")

    if len(argv) < 1:
        argv = sys.argv[1:]

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return RESULT_FAIL

    try:
        with open(args.input, encoding=args.encoding) as f:
            message = f.read()
    except UnicodeDecodeError:
        print(
            f"""
{Colors.LRED}[Bad Commit message encoding] {Colors.RESTORE}

{Colors.YELLOW}It looks like we couldn't decode your commit message using the encoding you or your system specified.
You can specify an encoding using the --encoding flag.{Colors.RESTORE}

For example, if your commit message is encoded in {Colors.YELLOW}UTF-8{Colors.RESTORE},
you can add this to your .pre-commit-config.yaml file:

  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: xxx
    hooks:
      - id: conventional-pre-commit
        stages: [ commit-msg ]
        args: [ {Colors.YELLOW}--encoding=utf-8, {Colors.RESTORE}custom-types, ... ]
        """
        )
        return RESULT_FAIL

    if format.is_conventional(message, args.types):
        return RESULT_SUCCESS
    else:
        print(
            f"""
        {Colors.LRED}[Bad Commit message] >>{Colors.RESTORE} {message}
        {Colors.YELLOW}Your commit message does not follow Conventional Commits formatting
        {Colors.LBLUE}https://www.conventionalcommits.org/{Colors.YELLOW}

        Conventional Commits start with one of the below types, followed by a colon,
        followed by the commit message:{Colors.RESTORE}

            {" ".join(format.conventional_types(args.types))}

        {Colors.YELLOW}Example commit message adding a feature:{Colors.RESTORE}

            feat: implement new API

        {Colors.YELLOW}Example commit message fixing an issue:{Colors.RESTORE}

            fix: remove infinite loop

        {Colors.YELLOW}Optionally, include a scope in parentheses after the type for more context:{Colors.RESTORE}

            fix(account): remove infinite loop"""
        )
        return RESULT_FAIL


if __name__ == "__main__":
    raise SystemExit(main())
