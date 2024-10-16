import os
from conventional_pre_commit.output import fail, fail_verbose, unicode_decode_error


def test_fail():
    output = fail("commit msg")

    assert "Bad commit message" in output
    assert "commit msg" in output
    assert "Conventional Commits formatting" in output
    assert "https://www.conventionalcommits.org/" in output


def test_fail_verbose():
    output = fail_verbose("commit msg", optional_scope=False)

    assert "Conventional Commit messages follow a pattern like" in output
    assert f"type(scope): subject{os.linesep}{os.linesep}    extended body" in output
    assert "Expected value for 'type' but found none." in output
    assert "Expected value for 'delim' but found none." in output
    assert "Expected value for 'scope' but found none." in output
    assert "Expected value for 'subject' but found none." in output
    assert "git commit --edit --file=.git/COMMIT_EDITMSG" in output
    assert "edit the commit message and retry the commit" in output


def test_fail_verbose__optional_scope():
    output = fail_verbose("commit msg", optional_scope=True)

    assert "Expected value for 'scope' but found none." not in output


def test_fail_verbose__missing_subject():
    output = fail_verbose("feat(scope):", optional_scope=False)

    assert "Expected value for 'subject' but found none." in output
    assert "Expected value for 'type' but found none." not in output
    assert "Expected value for 'scope' but found none." not in output


def test_fail_verbose_no_body_sep():
    output = fail_verbose(
        """feat(scope): subject
body without blank line
""",
        optional_scope=False,
    )

    assert "Expected value for 'sep' but found none." in output
    assert "Expected value for 'multi' but found none." not in output

    assert "Expected value for 'subject' but found none." not in output
    assert "Expected value for 'type' but found none." not in output
    assert "Expected value for 'scope' but found none." not in output


def test_unicode_decode_error():
    output = unicode_decode_error()

    assert "Bad commit message encoding" in output
    assert "UTF-8 encoding is assumed" in output
    assert "https://git-scm.com/docs/git-commit/#_discussion" in output
