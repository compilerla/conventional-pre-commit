import re

import pytest

from conventional_pre_commit.format import Commit, ConventionalCommit, is_conventional

CUSTOM_TYPES = ["one", "two"]


@pytest.fixture
def commit() -> Commit:
    return Commit()


@pytest.fixture
def conventional_commit() -> ConventionalCommit:
    return ConventionalCommit()


@pytest.fixture
def conventional_commit_scope_required(conventional_commit) -> ConventionalCommit:
    conventional_commit.scope_optional = False
    return conventional_commit


def test_commit_init():
    input = (
        """feat: some commit message
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch main
# Your branch is up to date with 'origin/main'.
#
# Changes to be committed:
#	modified:   README.md
#
# Changes not staged for commit:
#	modified:   README.md
#
# ------------------------ >8 ------------------------
# Do not modify or remove the line above.
# Everything below it will be ignored.
diff --git c/README.md i/README.md
index ea80a93..fe8a527 100644
--- c/README.md
+++ i/README.md
@@ -20,3 +20,4 @@ Some hunk header
 Context 1
"""
        + " "  # This is on purpose to preserve the space from overly eager stripping.
        + """
 Context 2
+Added line
"""
    )

    expected = "feat: some commit message\n"

    assert Commit(input).message == expected


def test_r_or(commit):
    result = commit._r_or(CUSTOM_TYPES)
    regex = re.compile(result)

    for item in CUSTOM_TYPES:
        assert regex.match(item)


def test_r_autosquash_prefixes(commit):
    regex = re.compile(commit.r_autosquash_prefixes)

    for prefix in commit.AUTOSQUASH_PREFIXES:
        assert regex.match(prefix)


def test_r_comment_single(commit):
    regex = re.compile(commit.r_comment)
    assert regex.match("# Some comment")
    assert not regex.match("Some comment")
    assert not regex.match(" # Some comment")


def test_strip_comments__consecutive(commit):
    input = """feat(scope): message
# Please enter the commit message for your changes.
# These are comments usually added by editors, f.ex. with export EDITOR=vim
    """
    result = commit._strip_comments(input)
    assert result.count("\n") == 1
    assert result.strip() == "feat(scope): message"


def test_strip_comments__spaced(commit):
    input = """feat(scope): message
# Please enter the commit message for your changes.

# These are comments usually added by editors, f.ex. with export EDITOR=vim
    """
    result = commit._strip_comments(input)
    assert result.count("\n") == 2
    assert result.strip() == "feat(scope): message"


def test_r_verbose_commit_ignored__does_not_match_no_verbose(commit):
    regex = re.compile(commit.r_verbose_commit_ignored, re.DOTALL | re.MULTILINE)
    input = """feat: some commit message
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch main
# Your branch is up to date with 'origin/main'.
#
# Changes to be committed:
#	modified:   README.md
#
# Changes not staged for commit:
#	modified:   README.md
#
"""

    assert not regex.search(input)


def test_r_verbose_commit_ignored__matches_single_verbose_ignored(commit):
    regex = re.compile(commit.r_verbose_commit_ignored, re.DOTALL | re.MULTILINE)
    input = (
        """feat: some commit message
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch main
# Your branch is up to date with 'origin/main'.
#
# Changes to be committed:
#	modified:   README.md
#
# Changes not staged for commit:
#	modified:   README.md
#
# ------------------------ >8 ------------------------
# Do not modify or remove the line above.
# Everything below it will be ignored.
diff --git c/README.md i/README.md
index ea80a93..fe8a527 100644
--- c/README.md
+++ i/README.md
@@ -20,3 +20,4 @@ Some hunk header
 Context 1
"""
        + " "  # This is on purpose to preserve the space from overly eager stripping.
        + """
 Context 2
+Added line
"""
    )

    assert regex.search(input)


def test_r_verbose_commit_ignored__matches_double_verbose_ignored(commit):
    regex = re.compile(commit.r_verbose_commit_ignored, re.DOTALL | re.MULTILINE)
    input = (
        """feat: some commit message
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch main
# Your branch is up to date with 'origin/main'.
#
# Changes to be committed:
#	modified:   README.md
#
# Changes not staged for commit:
#	modified:   README.md
#
# ------------------------ >8 ------------------------
# Do not modify or remove the line above.
# Everything below it will be ignored.
#
# Changes to be committed:
diff --git c/README.md i/README.md
index ea80a93..fe8a527 100644
--- c/README.md
+++ i/README.md
@@ -20,3 +20,4 @@ Some staged hunk header
 Staged Context 1
"""
        + " "  # This is on purpose to preserve the space from overly eager stripping.
        + """
 Staged Context 2
+Staged added line
# --------------------------------------------------
# Changes not staged for commit:
diff --git i/README.md w/README.md
index fe8a527..1c00c14 100644
--- i/README.md
+++ w/README.md
@@ -10,6 +10,7 @@ Some unstaged hunk header
 Context 1
 Context 2
 Context 3
-Removed line
+Added line
"""
        + " "  # This is on purpose to preserve the space from overly eager stripping.
        + """
 Context 4
"""
        + " "  # This is on purpose to preserve the space from overly eager stripping.
        + """
"""
    )

    assert regex.search(input)


def test_strip_verbose_commit_ignored__does_not_strip_no_verbose(commit):
    input = """feat: some commit message
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch main
# Your branch is up to date with 'origin/main'.
#
# Changes to be committed:
#	modified:   README.md
#
# Changes not staged for commit:
#	modified:   README.md
#
"""

    expected = """feat: some commit message
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch main
# Your branch is up to date with 'origin/main'.
#
# Changes to be committed:
#	modified:   README.md
#
# Changes not staged for commit:
#	modified:   README.md
#
"""

    result = commit._strip_verbose_commit_ignored(input)
    assert result == expected


def test_strip_verbose_commit_ignored__strips_single_verbose_ignored(commit):
    input = (
        """feat: some commit message
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch main
# Your branch is up to date with 'origin/main'.
#
# Changes to be committed:
#	modified:   README.md
#
# Changes not staged for commit:
#	modified:   README.md
#
# ------------------------ >8 ------------------------
# Do not modify or remove the line above.
# Everything below it will be ignored.
diff --git c/README.md i/README.md
index ea80a93..fe8a527 100644
--- c/README.md
+++ i/README.md
@@ -20,3 +20,4 @@ Some hunk header
 Context 1
"""
        + " "  # This is on purpose to preserve the space from overly eager stripping.
        + """
 Context 2
+Added line
"""
    )

    expected = """feat: some commit message
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch main
# Your branch is up to date with 'origin/main'.
#
# Changes to be committed:
#	modified:   README.md
#
# Changes not staged for commit:
#	modified:   README.md
#
"""

    result = commit._strip_verbose_commit_ignored(input)
    assert result == expected


def test_strip_verbose_commit_ignored__strips_double_verbose_ignored(commit):
    input = (
        """feat: some commit message
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch main
# Your branch is up to date with 'origin/main'.
#
# Changes to be committed:
#	modified:   README.md
#
# Changes not staged for commit:
#	modified:   README.md
#
# ------------------------ >8 ------------------------
# Do not modify or remove the line above.
# Everything below it will be ignored.
#
# Changes to be committed:
diff --git c/README.md i/README.md
index ea80a93..fe8a527 100644
--- c/README.md
+++ i/README.md
@@ -20,3 +20,4 @@ Some staged hunk header
 Staged Context 1
"""
        + " "  # This is on purpose to preserve the space from overly eager stripping.
        + """
 Staged Context 2
+Staged added line
# --------------------------------------------------
# Changes not staged for commit:
diff --git i/README.md w/README.md
index fe8a527..1c00c14 100644
--- i/README.md
+++ w/README.md
@@ -10,6 +10,7 @@ Some unstaged hunk header
 Context 1
 Context 2
 Context 3
-Removed line
+Added line
"""
        + " "  # This is on purpose to preserve the space from overly eager stripping.
        + """
 Context 4
"""
        + " "  # This is on purpose to preserve the space from overly eager stripping.
        + """
"""
    )

    expected = """feat: some commit message
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# On branch main
# Your branch is up to date with 'origin/main'.
#
# Changes to be committed:
#	modified:   README.md
#
# Changes not staged for commit:
#	modified:   README.md
#
"""

    result = commit._strip_verbose_commit_ignored(input)
    assert result == expected


@pytest.mark.parametrize(
    "input,expected_result",
    [
        ("amend! ", True),
        ("fixup! ", True),
        ("squash! ", True),
        ("squash! whatever .. $12 #", True),
        ("squash!", False),
        (" squash! ", False),
        ("squash!:", False),
        ("feat(foo):", False),
    ],
)
def test_has_autosquash_prefix(commit, input, expected_result):
    assert commit.has_autosquash_prefix(input) is expected_result
    assert Commit(input).has_autosquash_prefix() is expected_result


@pytest.mark.parametrize(
    "input,expected_result",
    [
        ("Merge branch '2.x.x' into '1.x.x'", True),
        ("merge branch 'dev' into 'main'", True),
        ("Merge remote-tracking branch 'origin/master'", True),
        ("Merge pull request #123 from user/feature-branch", True),
        ("Merge tag 'v1.2.3' into main", True),
        ("Merge origin/master into develop", True),
        ("Merge refs/heads/main into develop", True),
        ("nope not a merge commit", False),
        ("type: subject", False),
        ("fix: merge bug in auth logic", False),
        ("chore: merged upstream changes", False),
        ("MergeSort implemented and tested", False),
    ],
)
def test_is_merge_commit(input, expected_result):
    commit = Commit(input)
    assert commit.is_merge() is expected_result


def test_r_scope__optional(conventional_commit):
    regex = re.compile(conventional_commit.r_scope)

    assert regex.match("")


def test_r_scope__not_optional(conventional_commit_scope_required):
    regex = re.compile(conventional_commit_scope_required.r_scope)

    assert not regex.match("")
    assert not regex.match("scope")
    assert regex.match("(scope)")


def test_r_scope__alphanumeric(conventional_commit_scope_required):
    regex = re.compile(conventional_commit_scope_required.r_scope)

    assert regex.match("(50m3t41N6)")


def test_r_scope__special_chars(conventional_commit_scope_required):
    regex = re.compile(conventional_commit_scope_required.r_scope)

    assert regex.match("(some-thing)")
    assert regex.match("(some_thing)")
    assert regex.match("(some/thing)")
    assert regex.match("(some thing)")
    assert regex.match("(some:thing)")
    assert regex.match("(some,thing)")


def test_r_scope__scopes(conventional_commit_scope_required):
    conventional_commit_scope_required.scopes = ["api", "client"]
    regex = re.compile(conventional_commit_scope_required.r_scope)

    assert regex.match("(api)")
    assert regex.match("(client)")
    assert regex.match("(api, client)")
    assert regex.match("(api: client)")
    assert regex.match("(api/client)")
    assert regex.match("(api-client)")
    assert not regex.match("(test)")
    assert not regex.match("(api; client)")


def test_r_scope__scopes_uppercase(conventional_commit_scope_required):
    conventional_commit_scope_required.scopes = ["api", "client"]
    regex = re.compile(conventional_commit_scope_required.r_scope)

    assert regex.match("(API)")
    assert regex.match("(CLIENT)")
    assert regex.match("(API, CLIENT)")
    assert regex.match("(API: CLIENT)")
    assert regex.match("(API/CLIENT)")
    assert regex.match("(API-CLIENT)")
    assert not regex.match("(TEST)")
    assert not regex.match("(API; CLIENT)")


def test_r_delim(conventional_commit):
    regex = re.compile(conventional_commit.r_delim)

    assert regex.match(":")
    assert not regex.match("")


def test_r_delim__optional_breaking_indicator(conventional_commit):
    regex = re.compile(conventional_commit.r_delim)

    assert regex.match("!:")


def test_r_subject__starts_with_space(conventional_commit):
    regex = re.compile(conventional_commit.r_subject)

    assert not regex.match("something")
    assert regex.match(" something")


def test_r_subject__alphanumeric(conventional_commit):
    regex = re.compile(conventional_commit.r_subject)

    assert regex.match(" 50m3t41N6")


def test_r_subject__special_chars(conventional_commit):
    regex = re.compile(conventional_commit.r_subject)

    assert regex.match(" some-thing")
    assert regex.match(" some_thing")
    assert regex.match(" some/thing")
    assert regex.match(" some thing")


def test_types__default():
    assert ConventionalCommit().types == ConventionalCommit.DEFAULT_TYPES


def test_types__custom():
    result = ConventionalCommit(types=["custom"])

    assert set(["custom", *ConventionalCommit.CONVENTIONAL_TYPES]) == set(result.types)


def test_regex(conventional_commit):
    regex = conventional_commit.regex

    assert isinstance(regex, re.Pattern)
    assert "type" in regex.groupindex
    assert "scope" in regex.groupindex
    assert "delim" in regex.groupindex
    assert "subject" in regex.groupindex
    assert "body" in regex.groupindex
    assert "multi" in regex.groupindex
    assert "sep" in regex.groupindex


def test_match(conventional_commit):
    match = conventional_commit.match("test: subject line")

    assert isinstance(match, re.Match)
    assert match.group("type") == "test"
    assert match.group("scope") == ""
    assert match.group("delim") == ":"
    assert match.group("subject").strip() == "subject line"
    assert match.group("body") == ""


def test_match_multiline(conventional_commit):
    match = conventional_commit.match(
        """test(scope): subject line

body copy
"""
    )
    assert isinstance(match, re.Match)
    assert match.group("type") == "test"
    assert match.group("scope") == "(scope)"
    assert match.group("delim") == ":"
    assert match.group("subject").strip() == "subject line"
    assert match.group("body").strip() == "body copy"


def test_match_invalid_type(conventional_commit):
    match = conventional_commit.match(
        """invalid(scope): subject line

body copy
"""
    )
    assert isinstance(match, re.Match)
    assert match.group("type") is None
    assert match.group("scope") == ""
    assert match.group("delim") is None
    assert match.group("subject") is None
    assert match.group("body") == ""


@pytest.mark.parametrize("type", ConventionalCommit.DEFAULT_TYPES)
def test_is_valid__default_type(conventional_commit, type):
    input = f"{type}: message"

    assert conventional_commit.is_valid(input)


@pytest.mark.parametrize("type", ConventionalCommit.DEFAULT_TYPES)
def test_is_valid__default_type_uppercase(conventional_commit, type):
    input = f"{type.upper()}: message"

    assert conventional_commit.is_valid(input)


@pytest.mark.parametrize("type", ConventionalCommit.CONVENTIONAL_TYPES)
def test_is_valid__conventional_type(conventional_commit, type):
    input = f"{type}: message"

    assert conventional_commit.is_valid(input)


@pytest.mark.parametrize("type", ConventionalCommit.CONVENTIONAL_TYPES)
def test_is_valid__conventional_type_uppercase(conventional_commit, type):
    input = f"{type.upper()}: message"

    assert conventional_commit.is_valid(input)


@pytest.mark.parametrize("type", CUSTOM_TYPES)
def test_is_valid__custom_type(type):
    input = f"{type}: message"
    conventional_commits = ConventionalCommit(types=CUSTOM_TYPES)

    assert conventional_commits.is_valid(input)


@pytest.mark.parametrize("type", ConventionalCommit.CONVENTIONAL_TYPES)
def test_is_valid__conventional_custom_type(type):
    input = f"{type}: message"
    conventional_commits = ConventionalCommit(types=CUSTOM_TYPES)

    assert conventional_commits.is_valid(input)


@pytest.mark.parametrize("type", ConventionalCommit.CONVENTIONAL_TYPES)
def test_is_valid__conventional_custom_type_uppercase(type):
    input = f"{type.upper()}: message"
    conventional_commits = ConventionalCommit(types=CUSTOM_TYPES)

    assert conventional_commits.is_valid(input)


def test_is_valid__breaking_change(conventional_commit):
    input = "fix!: message"

    assert conventional_commit.is_valid(input)


def test_is_valid__with_scope(conventional_commit):
    input = "feat(scope): message"

    assert conventional_commit.is_valid(input)


def test_is_valid__body_multiline_body_bad_type(conventional_commit):
    input = """wrong: message

    more_message
    """

    assert not conventional_commit.is_valid(input)


def test_is_valid__bad_body_multiline(conventional_commit):
    input = """feat(scope): message
    more message
    """

    assert not conventional_commit.is_valid(input)


def test_is_valid__body_multiline(conventional_commit):
    input = """feat(scope): message

    more message
    """

    assert conventional_commit.is_valid(input)


def test_is_valid__bad_body_multiline_paragraphs(conventional_commit):
    input = """feat(scope): message
    more message

    more body message
    """

    assert not conventional_commit.is_valid(input)


def test_is_valid__comment(conventional_commit):
    input = """feat(scope): message
# Please enter the commit message for your changes.
# These are comments usually added by editors, f.ex. with export EDITOR=vim
"""
    assert conventional_commit.is_valid(input)


@pytest.mark.parametrize("char", ['"', "'", "`", "#", "&"])
def test_is_valid__body_special_char(conventional_commit, char):
    input = f"feat: message with {char}"

    assert conventional_commit.is_valid(input)


def test_is_valid__wrong_type(conventional_commit):
    input = "wrong: message"

    assert not conventional_commit.is_valid(input)


def test_is_valid__scope_special_chars(conventional_commit):
    input = "feat(%&*@()): message"

    assert not conventional_commit.is_valid(input)


def test_is_valid__space_scope(conventional_commit):
    input = "feat (scope): message"

    assert not conventional_commit.is_valid(input)


def test_is_valid__scope_space(conventional_commit):
    input = "feat(scope) : message"

    assert not conventional_commit.is_valid(input)


def test_is_valid__scope_not_optional(conventional_commit_scope_required):
    input = "feat: message"

    assert not conventional_commit_scope_required.is_valid(input)


def test_is_valid__scope_not_optional_empty_parenthesis(conventional_commit_scope_required):
    input = "feat(): message"

    assert not conventional_commit_scope_required.is_valid(input)


def test_is_valid__missing_delimiter(conventional_commit):
    input = "feat message"

    assert not conventional_commit.is_valid(input)


@pytest.mark.parametrize(
    "input,expected_result",
    [
        ("feat: subject", True),
        ("feat(scope): subject", True),
        (
            """feat(scope): subject

            extended body
            """,
            True,
        ),
        ("feat", False),
        ("feat subject", False),
        ("feat(scope): ", False),
        (": subject", False),
        ("(scope): subject", False),
        (
            """feat(scope): subject
            extended body no newline
            """,
            False,
        ),
    ],
)
def test_is_conventional(input, expected_result):
    assert is_conventional(input) == expected_result
