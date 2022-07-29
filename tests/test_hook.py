from conventional_pre_commit.hook import RESULT_SUCCESS, RESULT_FAIL, main


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
