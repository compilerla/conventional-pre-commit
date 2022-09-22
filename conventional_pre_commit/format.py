import re

CONVENTIONAL_TYPES = ["feat", "fix"]
DEFAULT_TYPES = [
    "build",
    "chore",
    "ci",
    "docs",
    "feat",
    "fix",
    "perf",
    "refactor",
    "revert",
    "style",
    "test",
]


def r_types(types):
    """Join types with pipe "|" to form regex ORs."""
    return "|".join(types)


def r_scope():
    """Regex str for an optional (scope)."""
    return r"(\([\w \/:-]+\))?"


def r_delim():
    """Regex str for optional breaking change indicator and colon delimiter."""
    return r"!?:"


def r_subject():
    """Regex str for subject line, body, footer."""
    return r" .+"


def conventional_types(types=[]):
    """Return a list of Conventional Commits types merged with the given types."""
    if set(types) & set(CONVENTIONAL_TYPES) == set():
        return CONVENTIONAL_TYPES + types
    return types


def is_conventional(input, types=DEFAULT_TYPES):
    """
    Returns True if input matches Conventional Commits formatting
    https://www.conventionalcommits.org

    Optionally provide a list of additional custom types.
    """
    types = conventional_types(types)
    pattern = f"^({r_types(types)}){r_scope()}{r_delim()}{r_subject()}$"
    regex = re.compile(pattern, re.DOTALL)

    return bool(regex.match(input))
