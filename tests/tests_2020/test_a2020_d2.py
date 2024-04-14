import pytest
from models.aoc_2020 import PasswordPolicy


@pytest.mark.parametrize("valid_password", ["abc", "bcaca", "abaa"])
def test_valid_password_has_required_letter_between_min_and_max_occurrences(
    valid_password,
):
    policy = PasswordPolicy(letter="a", min_occurrences=1, max_occurrences=3)
    assert policy.is_valid(valid_password)


@pytest.mark.parametrize("invalid_password", ["def", "baacaca"])
def test_invalid_password_does_not_have_required_letter_between_min_and_max_occurrences(
    invalid_password,
):
    policy = PasswordPolicy(letter="a", min_occurrences=1, max_occurrences=3)
    assert not policy.is_valid(invalid_password)
