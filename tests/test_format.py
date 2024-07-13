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


def test_r_scope__not_optional():
    result = format.r_scope(optional=False)
    regex = re.compile(result)

    # Assert not optional anymore
    assert not regex.match("")


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
    assert regex.match("(some,thing)")


def test_r_scope__scopes():
    scopes_input = ["api", "client"]
    result = format.r_scope(scopes=scopes_input)
    regex = re.compile(result)
    assert regex.match("(api)")
    assert regex.match("(client)")
    assert regex.match("(api, client)")
    assert regex.match("(api: client)")
    assert regex.match("(api/client)")
    assert regex.match("(api-client)")
    assert not regex.match("(test)")
    assert not regex.match("(api; client)")


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


def test_r_autosquash_prefixes():
    result = format.r_autosquash_prefixes()
    regex = re.compile(result)

    for prefix in format.AUTOSQUASH_PREFIXES:
        assert regex.match(prefix)


def test_merge_commit():
    assert format.is_merge_commit("Merge branch '2.x.x' into '1.x.x'")


def test_conventional_types__default():
    result = format.conventional_types()

    assert result == format.CONVENTIONAL_TYPES


def test_conventional_types__custom():
    result = format.conventional_types(["custom"])

    assert set(["custom", *format.CONVENTIONAL_TYPES]) == set(result)


def test_r_comment_single():
    regex = re.compile(format.r_comment())
    assert regex.match("# Some comment")
    assert not regex.match("Some comment")
    assert not regex.match(" # Some comment")


def test_strip_comments__consecutive():
    input = """feat(scope): message
# Please enter the commit message for your changes.
# These are comments usually added by editors, f.ex. with export EDITOR=vim
    """
    result = format.strip_comments(input)
    assert result.count("\n") == 1
    assert result.strip() == "feat(scope): message"


def test_strip_comments__spaced():
    input = """feat(scope): message
# Please enter the commit message for your changes.

# These are comments usually added by editors, f.ex. with export EDITOR=vim
    """
    result = format.strip_comments(input)
    assert result.count("\n") == 2
    assert result.strip() == "feat(scope): message"


def test_r_verbose_diff__has_diff():
    regex = re.compile(format.r_verbose_diff(), re.MULTILINE)
    input = """# ----------- >8 -----------
# Some comment
# Some comment
diff --git a/file b/file
"""

    assert regex.match(input)


def test_r_verbose_diff__no_diff():
    regex = re.compile(format.r_verbose_diff(), re.MULTILINE)
    input = """# ----------- >8 -----------
# Some comment
# Some comment
"""

    assert not regex.match(input)


def test_r_verbose_diff__no_extra_comments():
    regex = re.compile(format.r_verbose_diff(), re.MULTILINE)
    input = """# ----------- >8 -----------
diff --git a/file b/file
"""

    assert not regex.match(input)


def test_strip_verbose_diff__has_diff():
    input = """feat(scope): message
# Please enter the commit message for your changes.

# These are comments usually added by editors, f.ex. with export EDITOR=vim
# ----------- >8 -----------
# Some comment
# Some comment
diff --git a/file b/file
"""

    result = format.strip_verbose_diff(input)
    assert result.count("\n") == 4
    assert (
        result
        == """feat(scope): message
# Please enter the commit message for your changes.

# These are comments usually added by editors, f.ex. with export EDITOR=vim
"""
    )


def test_strip_verbose_diff__no_diff():
    input = """feat(scope): message
# Please enter the commit message for your changes.

# These are comments usually added by editors, f.ex. with export EDITOR=vim
# ----------- >8 -----------
# Some comment
# Some comment
"""

    result = format.strip_verbose_diff(input)
    assert result == input


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


def test_is_conventional__body_multiline_body_bad_type():
    input = """wrong: message

    more_message
    """

    assert not format.is_conventional(input)


def test_is_conventional__bad_body_multiline():
    input = """feat(scope): message
    more message
    """

    assert not format.is_conventional(input)


def test_is_conventional__body_multiline():
    input = """feat(scope): message

    more message
    """

    assert format.is_conventional(input)


def test_is_conventional__bad_body_multiline_paragraphs():
    input = """feat(scope): message
    more message

    more body message
    """

    assert not format.is_conventional(input)


def test_is_conventional__comment():
    input = """feat(scope): message
# Please enter the commit message for your changes.
# These are comments usually added by editors, f.ex. with export EDITOR=vim
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


def test_is_conventional__scope_not_optional():
    input = "feat: message"

    assert not format.is_conventional(input, optional_scope=False)


def test_is_conventional__scope_not_optional_empty_parenthesis():
    input = "feat(): message"

    assert not format.is_conventional(input, optional_scope=False)


def test_is_conventional__missing_delimiter():
    input = "feat message"

    assert not format.is_conventional(input)


@pytest.mark.parametrize(
    "input,has_prefix",
    [
        ("amend! ", True),
        ("fixup! ", True),
        ("squash! ", True),
        ("squash! whatever .. $12 #", True),
        ("squash!", False),
        (" squash! ", False),
        ("squash!:", False),
        ("feat(foo):", False),
    ],
)
def test_has_autosquash_prefix(input, has_prefix):
    assert format.has_autosquash_prefix(input) == has_prefix
