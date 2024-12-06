import pytest

from .brackets import mismatching_brackets, missing_brackets


@pytest.mark.parametrize(
    "valid_string",
    ["()", "[]", "{}", "({})", "[]{}", "{()()()}", "<([{}])>", "[<>({}){}[([])<>]]"],
)
def test_valid_string_has_no_mismatching_brackets(valid_string):
    assert list(mismatching_brackets(valid_string)) == []


@pytest.mark.parametrize(
    "incomplete_string",
    [
        "(",
        "[",
        "({}",
        "[]{",
        "{()()(",
        "<([{}]",
        "[<>({}){}[",
        "[({(<(())[]>[[{[]{<()<>>",
    ],
)
def test_incomplete_string_has_no_mismatching_brackets(incomplete_string):
    assert list(mismatching_brackets(incomplete_string)) == []


@pytest.mark.parametrize(
    "bad_string, mismatches",
    [
        ("(]", ["]"]),
        ("{()()()>", [">"]),
        ("<([]){()}[{>])", [">", ")"]),
    ],
)
def test_can_detect_mismatching_brackets_in_a_string(bad_string, mismatches):
    assert list(mismatching_brackets(bad_string)) == mismatches


@pytest.mark.parametrize(
    "valid_string",
    ["()", "[]", "{}", "({})", "[]{}", "{()()()}", "<([{}])>", "[<>({}){}[([])<>]]"],
)
def test_valid_string_has_no_missing_brackets(valid_string):
    assert list(missing_brackets(valid_string)) == []


@pytest.mark.parametrize(
    "bad_string",
    [
        "(]",
        "{()()()>",
        "<([]){()}[{>])",
    ],
)
def test_invalid_string_has_no_missing_brackets(bad_string):
    assert list(missing_brackets(bad_string)) == []


@pytest.mark.parametrize(
    "incomplete_string, missing",
    [
        ("(", [")"]),
        ("[", ["]"]),
        ("({}", [")"]),
        ("[]{", ["}"]),
        ("{()()(", [")", "}"]),
        ("<([{}]", [")", ">"]),
        ("[<>({}){}[", ["]", "]"]),
        ("[({(<(())[]>[[{[]{<()<>>", ["}", "}", "]", "]", ")", "}", ")", "]"]),
    ],
)
def test_incomplete_string_has_missing_brackets(incomplete_string, missing):
    assert list(missing_brackets(incomplete_string)) == missing
