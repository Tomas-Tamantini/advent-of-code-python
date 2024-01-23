import pytest
from models.aoc_2018 import first_frequency_to_be_reached_twice


@pytest.mark.parametrize(
    "offsets, expected",
    [
        ([1, -1], 0),
        ([3, 3, 4, -2, -4], 10),
        ([-6, 3, 8, 5, -6], 5),
        ([7, 7, -2, -7, -4], 14),
    ],
)
def test_first_frequency_to_be_reached_twice_is_properly_calculated(offsets, expected):
    assert first_frequency_to_be_reached_twice(offsets) == expected
