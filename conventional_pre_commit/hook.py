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


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("types", nargs="*", default=format.DEFAULT_TYPES)
    parser.add_argument("input")
    args = parser.parse_args(argv)

    with open(args.input) as f:
        message = f.read()

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
    argv = sys.argv[1:]
    raise SystemExit(main(argv))
