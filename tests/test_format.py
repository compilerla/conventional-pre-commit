import re

import pytest

from conventional_pre_commit import format


CUSTOM_TYPES = ["one", "two"]


def test_r_types():
    result = format.r_types(CUSTOM_TYPES)
    regex = re.compile(result)

    assert regex.match("one")
    assert regex.match("two")


def test_r_scope__optional():
    result = format.r_scope()
    regex = re.compile(result)

    assert regex.match("")


def test_r_scope__parenthesis_required():
    result = format.r_scope()
    regex = re.compile(result)

    # without parens produces a match object with a 0 span
    # since the (scope) is optional
    without_parens = regex.match("something")
    assert without_parens.span() == (0, 0)

    # with parens produces a match object with a span
    # that covers the input string
    with_parens = regex.match("(something)")
    assert with_parens.span() == (0, 11)


def test_r_scope__alphanumeric():
    result = format.r_scope()
    regex = re.compile(result)

    assert regex.match("(50m3t41N6)")


def test_r_scope__special_chars():
    result = format.r_scope()
    regex = re.compile(result)

    assert regex.match("(some-thing)")
    assert regex.match("(some_thing)")
    assert regex.match("(some/thing)")
    assert regex.match("(some thing)")
    assert regex.match("(some:thing)")


def test_r_delim():
    result = format.r_delim()
    regex = re.compile(result)

    assert regex.match(":")


def test_r_delim__optional_breaking_indicator():
    result = format.r_delim()
    regex = re.compile(result)

    assert regex.match("!:")


def test_r_subject__starts_with_space():
    result = format.r_subject()
    regex = re.compile(result)

    assert not regex.match("something")
    assert regex.match(" something")


def test_r_subject__alphanumeric():
    result = format.r_subject()
    regex = re.compile(result)

    assert regex.match(" 50m3t41N6")


def test_r_subject__special_chars():
    result = format.r_subject()
    regex = re.compile(result)

    assert regex.match(" some-thing")
    assert regex.match(" some_thing")
    assert regex.match(" some/thing")
    assert regex.match(" some thing")


def test_conventional_types__default():
    result = format.conventional_types()

    assert result == format.CONVENTIONAL_TYPES


def test_conventional_types__custom():
    result = format.conventional_types(["custom"])

    assert set(["custom", *format.CONVENTIONAL_TYPES]) == set(result)


@pytest.mark.parametrize("type", format.DEFAULT_TYPES)
def test_is_conventional__default_type(type):
    input = f"{type}: message"

    assert format.is_conventional(input)


@pytest.mark.parametrize("type", format.CONVENTIONAL_TYPES)
def test_is_conventional__conventional_type(type):
    input = f"{type}: message"

    assert format.is_conventional(input)


@pytest.mark.parametrize("type", CUSTOM_TYPES)
def test_is_conventional__custom_type(type):
    input = f"{type}: message"

    assert format.is_conventional(input, CUSTOM_TYPES)


@pytest.mark.parametrize("type", format.CONVENTIONAL_TYPES)
def test_is_conventional__conventional_custom_type(type):
    input = f"{type}: message"

    assert format.is_conventional(input, CUSTOM_TYPES)


def test_is_conventional__breaking_change():
    input = "fix!: message"

    assert format.is_conventional(input)


def test_is_conventional__with_scope():
    input = "feat(scope): message"

    assert format.is_conventional(input)


def test_is_conventional__body_multiline():
    input = """feat(scope): message

    more message
    """

    assert format.is_conventional(input)


@pytest.mark.parametrize("char", ['"', "'", "`", "#", "&"])
def test_is_conventional__body_special_char(char):
    input = f"feat: message with {char}"

    assert format.is_conventional(input)


def test_is_conventional__wrong_type():
    input = "wrong: message"

    assert not format.is_conventional(input)


def test_is_conventional__scope_special_chars():
    input = "feat(%&*@()): message"

    assert not format.is_conventional(input)


def test_is_conventional__space_scope():
    input = "feat (scope): message"

    assert not format.is_conventional(input)


def test_is_conventional__scope_space():
    input = "feat(scope) : message"

    assert not format.is_conventional(input)


def test_is_conventional__missing_delimiter():
    input = "feat message"

    assert not format.is_conventional(input)
