import re
from typing import List, Optional

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


def _get_scope_pattern(scopes: Optional[List[str]] = None):
    scopes_str = r_types(scopes)
    escaped_delimiters = list(map(re.escape, [":", ",", "-", "/"]))  # type: ignore
    delimiters_pattern = r_types(escaped_delimiters)
    return rf"\(\s*(?:{scopes_str})(?:\s*(?:{delimiters_pattern})\s*(?:{scopes_str}))*\s*\)"


def r_scope(optional=True, scopes: Optional[List[str]] = None):
    """Regex str for an optional (scope)."""

    if scopes:
        scopes_pattern = _get_scope_pattern(scopes)
        if optional:
            return f"(?:{scopes_pattern})?"
        else:
            return scopes_pattern

    if optional:
        return r"(\([\w \/:,-]+\))?"
    else:
        return r"(\([\w \/:,-]+\))"


def r_delim():
    """Regex str for optional breaking change indicator and colon delimiter."""
    return r"!?:"


def r_subject():
    """Regex str for subject line."""
    return r" .+$"


def r_body():
    """Regex str for the body"""
    return r"(?P<multi>\r?\n(?P<sep>^$\r?\n)?.+)?"


def r_autosquash_prefixes():
    """Regex str for autosquash prefixes."""
    return "|".join(AUTOSQUASH_PREFIXES)


def r_verbose_commit_ignored():
    """Regex str for the ignored part of verbose commit message templates"""
    return r"^# -{24} >8 -{24}\r?\n.*\Z"


def strip_verbose_commit_ignored(input):
    """Strip the ignored part of verbose commit message templates."""
    return re.sub(r_verbose_commit_ignored(), "", input, flags=re.DOTALL | re.MULTILINE)


def r_comment():
    """Regex str for comment"""
    return r"^#.*\r?\n?"


def strip_comments(input):
    return re.sub(r_comment(), "", input, flags=re.MULTILINE)


def conventional_types(types=[]):
    """Return a list of Conventional Commits types merged with the given types."""
    if set(types) & set(CONVENTIONAL_TYPES) == set():
        return CONVENTIONAL_TYPES + types
    return types


def conventional_regex(types=DEFAULT_TYPES, optional_scope=True, scopes: Optional[List[str]] = None):
    types = conventional_types(types)

    types_pattern = f"^(?P<type>{r_types(types)})?"
    scope_pattern = f"(?P<scope>{r_scope(optional_scope, scopes=scopes)})?"
    delim_pattern = f"(?P<delim>{r_delim()})?"
    subject_pattern = f"(?P<subject>{r_subject()})?"
    body_pattern = f"(?P<body>{r_body()})?"
    pattern = types_pattern + scope_pattern + delim_pattern + subject_pattern + body_pattern

    return re.compile(pattern, re.MULTILINE)


def clean_input(input: str):
    """
    Prepares an input message for conventional commits format check.
    """
    input = strip_verbose_commit_ignored(input)
    input = strip_comments(input)
    return input


def conventional_match(input: str, types=DEFAULT_TYPES, optional_scope=True, scopes: Optional[List[str]] = None):
    """
    Returns an `re.Match` object for the input against the Conventional Commits format.
    """
    input = clean_input(input)
    regex = conventional_regex(types, optional_scope, scopes)
    return regex.match(input)


def is_conventional(input: str, types=DEFAULT_TYPES, optional_scope=True, scopes: Optional[List[str]] = None) -> bool:
    """
    Returns True if input matches Conventional Commits formatting
    https://www.conventionalcommits.org

    Optionally provide a list of additional custom types.
    """
    result = conventional_match(input, types, optional_scope, scopes)
    is_valid = bool(result)

    if result and result.group("multi") and not result.group("sep"):
        is_valid = False
    if result and not all(
        [result.group("type"), optional_scope or result.group("scope"), result.group("delim"), result.group("subject")]
    ):
        is_valid = False

    return is_valid


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

def is_merge_commit(input):
    """
    Returns True if input starts with 'Merge branch '.

    It doesn't check whether the rest of the input matches Conventional Commits
    formatting.
    """

    return input.startswith("Merge branch ")
