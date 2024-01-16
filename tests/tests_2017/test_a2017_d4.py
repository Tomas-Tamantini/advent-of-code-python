import pytest
from models.aoc_2017 import sentence_contains_no_duplicates


@pytest.mark.parametrize(
    "sentence, expected",
    [
        ("aa bb cc dd ee", True),
        ("aa bb cc dd aa", False),
        ("aa bb cc dd aaa", True),
    ],
)
def test_checks_whether_sentence_contains_no_duplicates(sentence, expected):
    assert sentence_contains_no_duplicates(sentence) == expected
