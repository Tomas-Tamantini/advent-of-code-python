import pytest

from models.common.io import CharacterGrid

from .logic import TopographicMap


def _build_topographic_map(map_str: str) -> TopographicMap:
    return TopographicMap(CharacterGrid(map_str.replace(".", "8")))


_map_a = """0123
            1234
            8765
            9876"""

_map_b = """...0...
            ...1...
            ...2...
            6543456
            7.....7
            8.....8
            9.....9"""

_map_c = """..90..9
            ...1.98
            ...2..7
            6543456
            765.987
            876....
            987...."""

_map_d = """10..9..
            2...8..
            3...7..
            4567654
            ...8..3
            ...9..2
            .....01"""

_map_e = """89010123
            78121874
            87430965
            96549874
            45678903
            32019012
            01329801
            10456732"""


@pytest.mark.parametrize(
    ("map_str", "expected_num_trails"),
    [(_map_a, 1), (_map_b, 2), (_map_c, 4), (_map_d, 3), (_map_e, 36)],
)
def test_topographic_map_iterates_through_all_hiking_trails(
    map_str, expected_num_trails
):
    topographic_map = _build_topographic_map(map_str)
    assert expected_num_trails == len(set(topographic_map.hiking_trails()))
