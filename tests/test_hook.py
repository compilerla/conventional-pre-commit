import subprocess

import pytest

from conventional_pre_commit.hook import RESULT_SUCCESS, RESULT_FAIL, main


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


def test_main_success__conventional_utf8(conventional_utf8_commit_path):
    result = main([conventional_utf8_commit_path])

    assert result == RESULT_SUCCESS


def test_main_fail__conventional_gbk(conventional_gbk_commit_path):
    result = main([conventional_gbk_commit_path])

    assert result == RESULT_FAIL
