import pytest

from .solution import contains_exactly_n_of_any_letter, differing_indices


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


@pytest.mark.parametrize(
    "string_a, string_b, expected",
    [
        ("abcde", "axcye", [1, 3]),
        ("fghij", "fguij", [2]),
        ("abcde", "abcde", []),
    ],
)
def test_can_list_indices_where_strings_are_different(string_a, string_b, expected):
    assert list(differing_indices(string_a, string_b)) == expected
