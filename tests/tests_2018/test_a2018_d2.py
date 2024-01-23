import pytest
from models.aoc_2018 import contains_exactly_n_of_any_letter


@pytest.mark.parametrize(
    "string, n, expected",
    [
        ("abcdef", 2, False),
        ("bababc", 2, True),
        ("bababc", 3, True),
        ("ababab", 2, False),
    ],
)
def test_contains_exactly_n_of_any_letter_is_properly_calculated(string, n, expected):
    assert contains_exactly_n_of_any_letter(string, n) == expected
