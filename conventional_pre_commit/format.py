import re
from typing import List


class Commit:
    """
    Base class for inspecting commit message formatting.
    """

    AUTOSQUASH_PREFIXES = sorted(
        [
            "amend",
            "fixup",
            "squash",
        ]
    )

    def __init__(self, commit_msg: str = ""):
        self.message = str(commit_msg)
        self.message = self.clean()

    @property
    def r_autosquash_prefixes(self):
        """Regex str for autosquash prefixes."""
        return self._r_or(self.AUTOSQUASH_PREFIXES)

    @property
    def r_verbose_commit_ignored(self):
        """Regex str for the ignored part of a verbose commit message."""
        return r"^# -{24} >8 -{24}\r?\n.*\Z"

    @property
    def r_comment(self):
        """Regex str for comments."""
        return r"^#.*\r?\n?"

    def _r_or(self, items):
        """Join items with pipe "|" to form regex ORs."""
        return "|".join(items)

    def _strip_comments(self, commit_msg: str = ""):
        """Strip comments from a commit message."""
        commit_msg = commit_msg or self.message
        return re.sub(self.r_comment, "", commit_msg, flags=re.MULTILINE)

    def _strip_verbose_commit_ignored(self, commit_msg: str = ""):
        """Strip the ignored part of a verbose commit message."""
        commit_msg = commit_msg or self.message
        return re.sub(self.r_verbose_commit_ignored, "", commit_msg, flags=re.DOTALL | re.MULTILINE)

    def clean(self, commit_msg: str = ""):
        """
        Removes comments and ignored verbose commit segments from a commit message.
        """
        commit_msg = commit_msg or self.message
        commit_msg = self._strip_verbose_commit_ignored(commit_msg)
        commit_msg = self._strip_comments(commit_msg)
        return commit_msg

    def has_autosquash_prefix(self, commit_msg: str = ""):
        """
        Returns True if input starts with one of the autosquash prefixes used in git.
        See the documentation, please https://git-scm.com/docs/git-rebase.
        """
        commit_msg = self.clean(commit_msg)
        pattern = f"^(({self.r_autosquash_prefixes})! ).*$"
        regex = re.compile(pattern, re.DOTALL)

        return bool(regex.match(commit_msg))

    def is_merge(self, commit_msg: str = ""):
        """
        Returns True if input starts with "Merge branch"
        See the documentation, please https://git-scm.com/docs/git-merge.
        """
        commit_msg = self.clean(commit_msg)
        return commit_msg.startswith("Merge branch ")


class ConventionalCommit(Commit):
    """
    Impelements checks for Conventional Commits formatting.

    https://www.conventionalcommits.org
    """

    CONVENTIONAL_TYPES = sorted(["feat", "fix"])
    DEFAULT_TYPES = sorted(
        CONVENTIONAL_TYPES
        + [
            "build",
            "chore",
            "ci",
            "docs",
            "perf",
            "refactor",
            "revert",
            "style",
            "test",
        ]
    )

    def __init__(self, commit_msg: str = "", types=DEFAULT_TYPES, scope_optional=True, scopes: List[str] = []):
        super().__init__(commit_msg)

        if set(types) & set(self.CONVENTIONAL_TYPES) == set():
            self.types = self.CONVENTIONAL_TYPES + types
        else:
            self.types = types
        self.types = sorted(self.types)
        self.scope_optional = scope_optional
        self.scopes = scopes

    @property
    def r_types(self):
        """Regex str for valid types."""
        return self._r_or(self.types)

    @property
    def r_scope(self):
        """Regex str for an optional (scope)."""
        if self.scopes:
            scopes = self._r_or(self.scopes)
            escaped_delimiters = list(map(re.escape, [":", ",", "-", "/"]))  # type: ignore
            delimiters_pattern = self._r_or(escaped_delimiters)
            scope_pattern = rf"\(\s*(?:{scopes})(?:\s*(?:{delimiters_pattern})\s*(?:{scopes}))*\s*\)"

            if self.scope_optional:
                return f"(?:{scope_pattern})?"
            else:
                return scope_pattern

        if self.scope_optional:
            return r"(\([\w \/:,-]+\))?"
        else:
            return r"(\([\w \/:,-]+\))"

    @property
    def r_delim(self):
        """Regex str for optional breaking change indicator and colon delimiter."""
        return r"!?:"

    @property
    def r_subject(self):
        """Regex str for subject line."""
        return r" .+$"

    @property
    def r_body(self):
        """Regex str for the body, with multiline support."""
        return r"(?P<multi>\r?\n(?P<sep>^$\r?\n)?.+)?"

    @property
    def regex(self):
        """`re.Pattern` for ConventionalCommits formatting."""
        types_pattern = f"^(?P<type>{self.r_types})?"
        scope_pattern = f"(?P<scope>{self.r_scope})?"
        delim_pattern = f"(?P<delim>{self.r_delim})?"
        subject_pattern = f"(?P<subject>{self.r_subject})?"
        body_pattern = f"(?P<body>{self.r_body})?"
        pattern = types_pattern + scope_pattern + delim_pattern + subject_pattern + body_pattern

        return re.compile(pattern, re.MULTILINE)

    def errors(self, commit_msg: str = ""):
        """
        Return a list of missing Conventional Commit components from a commit message.
        """
        match = self.match(commit_msg)
        groups = match.groupdict() if match else {}

        if self.scope_optional:
            groups.pop("scope", None)

        if not groups.get("body"):
            groups.pop("body", None)
            groups.pop("multi", None)
            groups.pop("sep", None)

        return [g for g, v in groups.items() if not v]

    def is_valid(self, commit_msg: str = "") -> bool:
        """
        Returns True if commit_msg matches Conventional Commits formatting.
        https://www.conventionalcommits.org
        """
        match = self.match(commit_msg)

        # match all the required components
        #
        #    type(scope): subject
        #
        #    extended body
        #
        return bool(match) and all(
            [
                match.group("type"),
                self.scope_optional or match.group("scope"),
                match.group("delim"),
                match.group("subject"),
                any(
                    [
                        # no extra body; OR
                        not match.group("body"),
                        # a multiline body with proper separator
                        match.group("multi") and match.group("sep"),
                    ]
                ),
            ]
        )

    def match(self, commit_msg: str = ""):
        """
        Returns an `re.Match` object for the input against the Conventional Commits format.
        """
        commit_msg = self.clean(commit_msg) or self.message
        return self.regex.match(commit_msg)


def is_conventional(
    input: str, types: List[str] = ConventionalCommit.DEFAULT_TYPES, optional_scope=True, scopes: List[str] = []
) -> bool:
    """
    Returns True if input matches Conventional Commits formatting
    https://www.conventionalcommits.org

    Optionally provide a list of additional custom types.
    """
    commit = ConventionalCommit(commit_msg=input, types=types, scope_optional=optional_scope, scopes=scopes)

    return commit.is_valid()
