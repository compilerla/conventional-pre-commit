import subprocess

import pytest

from conventional_pre_commit.hook import RESULT_FAIL, RESULT_SUCCESS, main


@pytest.fixture
def cmd():
    return "conventional-pre-commit"


def test_main_fail__missing_args():
    result = main()

    assert result == RESULT_FAIL


def test_main_fail__bad(bad_commit_path):
    result = main([bad_commit_path])

    assert result == RESULT_FAIL


def test_main_fail__custom(bad_commit_path):
    result = main(["custom", bad_commit_path])

    assert result == RESULT_FAIL


def test_main_success__conventional(conventional_commit_path):
    result = main([conventional_commit_path])

    assert result == RESULT_SUCCESS


def test_main_success__custom(custom_commit_path):
    result = main(["custom", custom_commit_path])

    assert result == RESULT_SUCCESS


def test_main_success__custom_conventional(conventional_commit_path):
    result = main(["custom", conventional_commit_path])

    assert result == RESULT_SUCCESS


def test_main_success__conventional_utf8(conventional_utf8_commit_path):
    result = main([conventional_utf8_commit_path])

    assert result == RESULT_SUCCESS


def test_main_fail__conventional_gbk(conventional_gbk_commit_path):
    result = main([conventional_gbk_commit_path])

    assert result == RESULT_FAIL


def test_main_fail__conventional_with_scope(conventional_commit_path):
    result = main(["--force-scope", conventional_commit_path])

    assert result == RESULT_FAIL


def test_main_success__conventional_with_scope(cmd, conventional_commit_with_scope_path):
    result = main(["--force-scope", conventional_commit_with_scope_path])

    assert result == RESULT_SUCCESS


def test_main_success__fixup_commit(fixup_commit_path):
    result = main([fixup_commit_path])

    assert result == RESULT_SUCCESS


def test_main_fail__fixup_commit(fixup_commit_path):
    result = main(["--strict", fixup_commit_path])

    assert result == RESULT_FAIL


def test_main_success__conventional_commit_multi_line(conventional_commit_multi_line_path):
    result = main([conventional_commit_multi_line_path])

    assert result == RESULT_SUCCESS


def test_main_fail__conventional_commit_bad_multi_line(conventional_commit_bad_multi_line_path):
    result = main([conventional_commit_bad_multi_line_path])

    assert result == RESULT_FAIL


def test_subprocess_fail__missing_args(cmd):
    result = subprocess.call(cmd)

    assert result == RESULT_FAIL


def test_subprocess_fail__bad(cmd, bad_commit_path):
    result = subprocess.call((cmd, bad_commit_path))

    assert result == RESULT_FAIL


def test_subprocess_fail__custom(cmd, bad_commit_path):
    result = subprocess.call((cmd, "custom", bad_commit_path))

    assert result == RESULT_FAIL


def test_subprocess_success__conventional(cmd, conventional_commit_path):
    result = subprocess.call((cmd, conventional_commit_path))

    assert result == RESULT_SUCCESS


def test_subprocess_success__custom(cmd, custom_commit_path):
    result = subprocess.call((cmd, "custom", custom_commit_path))

    assert result == RESULT_SUCCESS


def test_subprocess_success__custom_conventional(cmd, conventional_commit_path):
    result = subprocess.call((cmd, "custom", conventional_commit_path))

    assert result == RESULT_SUCCESS


def test_subprocess_fail__conventional_with_scope(cmd, conventional_commit_path):
    result = subprocess.call((cmd, "--force-scope", conventional_commit_path))

    assert result == RESULT_FAIL


def test_subprocess_success__conventional_with_scope(cmd, conventional_commit_with_scope_path):
    result = subprocess.call((cmd, "--force-scope", conventional_commit_with_scope_path))

    assert result == RESULT_SUCCESS


def test_subprocess_success__conventional_with_multiple_scopes(cmd, conventional_commit_with_multiple_scopes_path):
    result = subprocess.call((cmd, "--scopes", "api,client", conventional_commit_with_multiple_scopes_path))
    assert result == RESULT_SUCCESS


def test_subprocess_fail__conventional_with_multiple_scopes(cmd, conventional_commit_with_multiple_scopes_path):
    result = subprocess.call((cmd, "--scopes", "api", conventional_commit_with_multiple_scopes_path))
    assert result == RESULT_FAIL


def test_main_success__custom_scopes_optional_scope(conventional_commit_path):
    result = main(["--scopes", "api,client", conventional_commit_path])
    assert result == RESULT_SUCCESS


def test_main_success__custom_scopes_with_allowed_scope(conventional_commit_with_multiple_scopes_path):
    result = main(["--scopes", "chore,api,client", conventional_commit_with_multiple_scopes_path])
    assert result == RESULT_SUCCESS


def test_main_fail__custom_scopes_with_disallowed_scope(conventional_commit_with_scope_path):
    result = main(["--scopes", "api,client", conventional_commit_with_scope_path])
    assert result == RESULT_FAIL


def test_main_fail__custom_scopes_require_scope_no_scope(conventional_commit_path):
    result = main(["--scopes", "chore,feat,fix,custom", "--force-scope", conventional_commit_path])
    assert result == RESULT_FAIL


def test_main_success__custom_scopes_require_scope_with_allowed_scope(conventional_commit_with_scope_path):
    result = main(["--scopes", "api,client,scope", "--force-scope", conventional_commit_with_scope_path])
    assert result == RESULT_SUCCESS


def test_main_fail__custom_scopes_require_scope_with_disallowed_scope(conventional_commit_with_scope_path):
    result = main(["--scopes", "api,client", "--force-scope", conventional_commit_with_scope_path])
    assert result == RESULT_FAIL


def test_subprocess_success__fixup_commit(cmd, fixup_commit_path):
    result = subprocess.call((cmd, fixup_commit_path))

    assert result == RESULT_SUCCESS


def test_subprocess_fail__fixup_commit(cmd, fixup_commit_path):
    result = subprocess.call((cmd, "--strict", fixup_commit_path))

    assert result == RESULT_FAIL


def test_subprocess_success__conventional_commit_multi_line(cmd, conventional_commit_multi_line_path):
    result = subprocess.call((cmd, conventional_commit_multi_line_path))

    assert result == RESULT_SUCCESS


def test_subprocess_fail__conventional_commit_bad_multi_line(cmd, conventional_commit_bad_multi_line_path):
    result = subprocess.call((cmd, conventional_commit_bad_multi_line_path))

    assert result == RESULT_FAIL
