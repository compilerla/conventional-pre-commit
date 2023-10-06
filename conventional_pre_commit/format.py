import re
from typing import Iterator

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
AUTOSQUASH_PREFIXES = [
    "amend",
    "fixup",
    "squash",
]


def r_types(types):
    """Join types with pipe "|" to form regex ORs."""
    return "|".join(types)


def r_scope(optional=True):
    """Regex str for an optional (scope)."""
    if optional:
        return r"(\([\w \/:-]+\))?"
    else:
        return r"(\([\w \/:-]+\))"


def r_delim():
    """Regex str for optional breaking change indicator and colon delimiter."""
    return r"!?:"


def r_subject():
    """Regex str for subject line, body, footer."""
    return r" .+"


def r_autosquash_prefixes():
    """Regex str for autosquash prefixes."""
    return "|".join(AUTOSQUASH_PREFIXES)


def conventional_types(types=[]):
    """Return a list of Conventional Commits types merged with the given types."""
    if set(types) & set(CONVENTIONAL_TYPES) == set():
        return CONVENTIONAL_TYPES + types
    return types


def is_conventional(input, types=DEFAULT_TYPES, optional_scope=True):
    """
    Returns True if input matches Conventional Commits formatting
    https://www.conventionalcommits.org

    Optionally provide a list of additional custom types.
    """
    types = conventional_types(types)
    pattern = f"^({r_types(types)}){r_scope(optional_scope)}{r_delim()}{r_subject()}$"
    regex = re.compile(pattern, re.DOTALL)

    return bool(regex.match(input))


def has_autosquash_prefix(input):
    """
    Returns True if input starts with one of the autosquash prefixes used in git.
    See the documentation, please https://git-scm.com/docs/git-rebase.

    It doesn't check whether the rest of the input matches Conventional Commits
    formatting.
    """
    pattern = f"^(({r_autosquash_prefixes()})! ).*$"
    regex = re.compile(pattern, re.DOTALL)

    return bool(regex.match(input))


def remove_by_git_ignored_lines(input: str) -> str:
    """
    After finishing a commit message, git ignores certain parts
    and adds only the rest to the actual message stored.
    In order to prevent failed detection of valid commit messages,
    these postprocessing steps also need to get applied here
    before checking for valid Conventional Commits formatting.
    """

    def get_git_postprocessed_input(_input: str) -> Iterator[str]:
        first_non_empty_line_found = False
        for msg_line in _input.split("\n"):
            if not first_non_empty_line_found and not msg_line.strip():
                continue
            elif msg_line.strip().startswith("#"):
                continue
            else:
                first_non_empty_line_found = True
                yield msg_line

    return "\n".join(get_git_postprocessed_input(input))
