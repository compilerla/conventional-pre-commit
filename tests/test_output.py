from conventional_pre_commit.output import fail, fail_verbose, unicode_decode_error


def test_fail():
    output = fail("commit msg")

    assert "Bad commit message" in output
    assert "commit msg" in output
    assert "Conventional Commits formatting" in output
    assert "https://www.conventionalcommits.org/" in output


def test_fail_verbose():
    output = fail_verbose("commit msg")

    assert "git commit --edit --file=.git/COMMIT_EDITMSG" in output
    assert "edit the commit message and retry the commit" in output


def test_unicode_decode_error():
    output = unicode_decode_error()

    assert "Bad commit message encoding" in output
    assert "UTF-8 encoding is assumed" in output
    assert "https://git-scm.com/docs/git-commit/#_discussion" in output
