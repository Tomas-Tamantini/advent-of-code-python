import pytest
from models.aoc_2017 import HexDirection, num_hex_steps_away


def test_empty_path_is_away_zero_steps():
    assert list(num_hex_steps_away([])) == []


def test_single_path_step_is_away_one_step():
    assert list(num_hex_steps_away([HexDirection.SOUTHEAST])) == [1]


@pytest.mark.parametrize(
    "directions, expected_steps",
    [
        ([HexDirection.NORTH, HexDirection.NORTH], 2),
        ([HexDirection.SOUTH, HexDirection.NORTHWEST], 1),
        ([HexDirection.NORTHWEST, HexDirection.SOUTHEAST], 0),
    ],
)
def test_two_steps_path_may_be_reduced_to_one_or_zero_steps(directions, expected_steps):
    assert list(num_hex_steps_away(directions)) == [1, expected_steps]
