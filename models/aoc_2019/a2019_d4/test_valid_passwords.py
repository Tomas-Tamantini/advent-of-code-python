import pytest

from .valid_passwords import (
    at_least_one_group_of_exactly_two_equal_digits,
    digits_are_increasing,
    two_adjacent_digits_are_the_same,
    valid_passwords_in_range,
)


@pytest.mark.parametrize(
    "n, expected",
    [(123456, True), (123455, True), (123454, False)],
)
def test_can_check_whether_digits_are_increasing(n, expected):
    assert digits_are_increasing(n) == expected


@pytest.mark.parametrize(
    "n, expected",
    [(123456, False), (123455, True), (12232, True)],
)
def test_can_check_whether_two_adjacent_digits_are_the_same(n, expected):
    assert two_adjacent_digits_are_the_same(n) == expected


@pytest.mark.parametrize(
    "n, expected",
    [(123456, False), (123455, True), (122333, True), (123444, False)],
)
def test_can_check_whether_at_least_one_group_of_exactly_two_equal_digits(n, expected):
    assert at_least_one_group_of_exactly_two_equal_digits(n) == expected


def test_can_iterate_through_all_valid_passwords_in_given_range():
    criteria = [digits_are_increasing]
    assert len(list(valid_passwords_in_range(1, 99, criteria))) == 54
