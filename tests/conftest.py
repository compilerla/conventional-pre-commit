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
def custom_commit_path():
    return get_message_path("custom_commit")
