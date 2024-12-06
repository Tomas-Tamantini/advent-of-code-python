import pytest

from .solution import (
    sentence_contains_no_anagrams,
    sentence_contains_no_duplicates,
)


@pytest.mark.parametrize(
    ("sentence", "expected"),
    [
        ("aa bb cc dd ee", True),
        ("aa bb cc dd aa", False),
        ("aa bb cc dd aaa", True),
    ],
)
def test_checks_whether_sentence_contains_no_duplicates(sentence, expected):
    assert sentence_contains_no_duplicates(sentence) == expected


@pytest.mark.parametrize(
    ("sentence", "expected"),
    [
        ("abcde fghij", True),
        ("abcde xyz ecdab", False),
        ("a ab abc abd abf abj", True),
        ("iiii oiii ooii oooi oooo", True),
        ("oiii ioii iioi iiio", False),
    ],
)
def test_checks_whether_sentence_contains_no_anagrams(sentence, expected):
    assert sentence_contains_no_anagrams(sentence) == expected
