import os.path

import pytest

TEST_DIR = os.path.abspath(os.path.dirname(__file__))


def get_message_path(path):
    return os.path.join(TEST_DIR, "messages", path)


@pytest.fixture
def bad_commit_path():
    return get_message_path("bad_commit")


@pytest.fixture
def conventional_commit_path():
    return get_message_path("conventional_commit")


@pytest.fixture
def conventional_commit_with_scope_path():
    return get_message_path("conventional_commit_with_scope")


@pytest.fixture
def custom_commit_path():
    return get_message_path("custom_commit")


@pytest.fixture
def conventional_utf8_commit_path():
    return get_message_path("conventional_commit_utf-8")


@pytest.fixture
def conventional_gbk_commit_path():
    return get_message_path("conventional_commit_gbk")


@pytest.fixture
def fixup_commit_path():
    return get_message_path("fixup_commit")


@pytest.fixture
def conventional_commit_bad_multi_line_path():
    return get_message_path("conventional_commit_bad_multi_line")


@pytest.fixture
def conventional_commit_multi_line_path():
    return get_message_path("conventional_commit_multi_line")


@pytest.fixture
def conventional_commit_with_multiple_scopes_path():
    return get_message_path("conventional_commit_with_multiple_scopes")
