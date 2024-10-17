import os
from conventional_pre_commit.output import Colors, fail, fail_verbose, unicode_decode_error


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


def test_fail():
    output = fail("commit msg")

    assert Colors.LRED in output
    assert Colors.YELLOW in output
    assert Colors.LBLUE in output
    assert Colors.RESTORE in output

    assert "Bad commit message" in output
    assert "commit msg" in output
    assert "Conventional Commits formatting" in output
    assert "https://www.conventionalcommits.org/" in output


def test_fail__no_color():
    output = fail("commit msg", use_color=False)

    assert Colors.LRED not in output
    assert Colors.YELLOW not in output
    assert Colors.LBLUE not in output
    assert Colors.RESTORE not in output


def test_fail_verbose():
    output = fail_verbose("commit msg", optional_scope=False)

    assert Colors.YELLOW in output
    assert Colors.RESTORE in output

    output = output.replace(Colors.YELLOW, Colors.RESTORE).replace(Colors.RESTORE, "")

    assert "Conventional Commit messages follow a pattern like" in output
    assert f"type(scope): subject{os.linesep}{os.linesep}    extended body" in output
    assert "Expected value for type but found none." in output
    assert "Expected value for delim but found none." in output
    assert "Expected value for scope but found none." in output
    assert "Expected value for subject but found none." in output
    assert "git commit --edit --file=.git/COMMIT_EDITMSG" in output
    assert "edit the commit message and retry the commit" in output


def test_fail_verbose__no_color():
    output = fail_verbose("commit msg", use_color=False)

    assert Colors.LRED not in output
    assert Colors.YELLOW not in output
    assert Colors.LBLUE not in output
    assert Colors.RESTORE not in output


def test_fail_verbose__optional_scope():
    output = fail_verbose("commit msg", optional_scope=True, use_color=False)

    assert "Expected value for scope but found none." not in output


def test_fail_verbose__missing_subject():
    output = fail_verbose("feat(scope):", optional_scope=False, use_color=False)

    assert "Expected value for subject but found none." in output
    assert "Expected value for type but found none." not in output
    assert "Expected value for scope but found none." not in output


def test_fail_verbose__no_body_sep():
    output = fail_verbose(
        """feat(scope): subject
body without blank line
""",
        optional_scope=False,
        use_color=False,
    )

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
