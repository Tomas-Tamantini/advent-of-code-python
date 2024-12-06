import pytest

from ..password_policy import PositionalPasswordPolicy, RangePasswordPolicy


@pytest.mark.parametrize("valid_password", ["abc", "bcaca", "abaa"])
def test_valid_range_password_has_required_letter_between_min_and_max_occurrences(
    valid_password,
):
    policy = RangePasswordPolicy(letter="a", min_occurrences=1, max_occurrences=3)
    assert policy.is_valid(valid_password)


@pytest.mark.parametrize("invalid_password", ["def", "baacaca"])
def test_invalid_range_password_does_not_have_required_letter_between_min_and_max_occurrences(
    invalid_password,
):
    policy = RangePasswordPolicy(letter="a", min_occurrences=1, max_occurrences=3)
    assert not policy.is_valid(invalid_password)


@pytest.mark.parametrize("valid_password", ["abc", "bcaca", "baa"])
def test_valid_positional_password_has_required_letter_in_exactly_one_of_two_given_positions_with_base_one(
    valid_password,
):
    policy = PositionalPasswordPolicy(letter="a", first_position=1, second_position=3)
    assert policy.is_valid(valid_password)


@pytest.mark.parametrize("invalid_password", ["def", "aaacaca"])
def test_valid_positional_password_has_required_letter_in_zero_or_two_of_given_positions_with_base_one(
    invalid_password,
):
    policy = PositionalPasswordPolicy(letter="a", first_position=1, second_position=3)
    assert not policy.is_valid(invalid_password)
