import os

import pytest

from conventional_pre_commit.format import ConventionalCommit
from conventional_pre_commit.output import Colors, fail, fail_verbose, unicode_decode_error


@pytest.fixture
def commit():
    return ConventionalCommit("commit msg")


def test_colors():
    colors = Colors()

    assert colors.blue == colors.LBLUE
    assert colors.red == colors.LRED
    assert colors.restore == colors.RESTORE
    assert colors.yellow == colors.YELLOW

    colors = Colors(enabled=False)

    assert colors.blue == ""
    assert colors.red == ""
    assert colors.restore == ""
    assert colors.yellow == ""


def test_fail(commit):
    output = fail(commit)

    assert Colors.LRED in output
    assert Colors.YELLOW in output
    assert Colors.LBLUE in output
    assert Colors.RESTORE in output

    assert "Bad commit message" in output
    assert "commit msg" in output
    assert "Conventional Commits formatting" in output
    assert "https://www.conventionalcommits.org/" in output


def test_fail__no_color(commit):
    output = fail(commit, use_color=False)

    assert Colors.LRED not in output
    assert Colors.YELLOW not in output
    assert Colors.LBLUE not in output
    assert Colors.RESTORE not in output


def test_fail_verbose(commit):
    commit.scope_optional = False
    output = fail_verbose(commit)

    assert Colors.YELLOW in output
    assert Colors.RESTORE in output

    output = output.replace(Colors.YELLOW, Colors.RESTORE).replace(Colors.RESTORE, "")

    assert "Conventional Commit messages follow a pattern like" in output
    assert f"type(scope): subject{os.linesep}{os.linesep}    extended body" in output
    assert "Expected value for type from:" in output
    for t in commit.types:
        assert t in output
    assert "Expected value for scope but found none." in output
    assert "git commit --edit --file=.git/COMMIT_EDITMSG" in output
    assert "edit the commit message and retry the commit" in output


def test_fail_verbose__no_color(commit):
    output = fail_verbose(commit, use_color=False)

    assert Colors.LRED not in output
    assert Colors.YELLOW not in output
    assert Colors.LBLUE not in output
    assert Colors.RESTORE not in output


def test_fail_verbose__optional_scope(commit):
    commit.scope_optional = True
    output = fail_verbose(commit, use_color=False)

    assert "Expected value for scope but found none." not in output


def test_fail_verbose__missing_subject():
    commit = ConventionalCommit("feat(scope):", scope_optional=False)
    output = fail_verbose(commit, use_color=False)

    assert "Expected value for subject but found none." in output
    assert "Expected value for type but found none." not in output
    assert "Expected value for scope but found none." not in output


def test_fail_verbose__no_body_sep():
    commit = ConventionalCommit(
        scope_optional=False,
        commit_msg="""feat(scope): subject
body without blank line
""",
    )

    output = fail_verbose(commit, use_color=False)

    assert "Expected value for sep but found none." in output
    assert "Expected value for multi but found none." not in output

    assert "Expected value for subject but found none." not in output
    assert "Expected value for type but found none." not in output
    assert "Expected value for scope but found none." not in output


def test_unicode_decode_error():
    output = unicode_decode_error()

    assert Colors.LRED in output
    assert Colors.YELLOW in output
    assert Colors.LBLUE in output
    assert Colors.RESTORE in output

    assert "Bad commit message encoding" in output
    assert "UTF-8 encoding is assumed" in output
    assert "https://git-scm.com/docs/git-commit/#_discussion" in output


def test_unicode_decode_error__no_color():
    output = unicode_decode_error(use_color=False)

    assert Colors.LRED not in output
    assert Colors.YELLOW not in output
    assert Colors.LBLUE not in output
    assert Colors.RESTORE not in output
