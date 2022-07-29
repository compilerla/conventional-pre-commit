import argparse
import sys

from conventional_pre_commit import format

RESULT_SUCCESS = 0
RESULT_FAIL = 1


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
        return RESULT_FAIL


if __name__ == "__main__":
    argv = sys.argv[1:]
    raise SystemExit(main(argv))
