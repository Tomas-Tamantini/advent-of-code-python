import pytest

from .solution import (
    digits_that_match_one_across_the_circle,
    digits_that_match_the_next,
)


def test_if_all_digits_are_different_none_is_equal_to_next_one():
    assert list(digits_that_match_the_next("12345", wrap_around=False)) == []


def test_if_some_digits_come_in_pairs_of_two_they_are_equal_to_next_one():
    assert list(digits_that_match_the_next("11122", wrap_around=False)) == [
        "1",
        "1",
        "2",
    ]


def test_last_digit_can_be_compared_with_first():
    assert list(digits_that_match_the_next("12341", wrap_around=False)) == []
    assert list(digits_that_match_the_next("12341", wrap_around=True)) == ["1"]


@pytest.mark.parametrize(
    "sequence, expected",
    [
        ("1212", ["1", "2", "1", "2"]),
        ("1221", []),
        ("123425", ["2", "2"]),
        ("123123", ["1", "2", "3", "1", "2", "3"]),
        ("12131415", ["1", "1", "1", "1"]),
    ],
)
def test_digits_can_be_checked_against_one_across_the_circle(sequence, expected):
    assert list(digits_that_match_one_across_the_circle(sequence)) == expected
