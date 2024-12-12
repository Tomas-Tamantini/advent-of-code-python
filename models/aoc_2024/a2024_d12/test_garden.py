import pytest

from models.common.io import CharacterGrid

from .garden import Garden

_garden_a = """AAAA
               BBCD
               BBCC
               EEEC"""

_garden_b = """OOOOO
               OXOXO
               OOOOO
               OXOXO
               OOOOO"""

_garden_c = """RRRRIICCFF
               RRRRIICCCF
               VVRRRCCFFF
               VVRCCCJFFF
               VVVVCJJCFE
               VVIVCCJJEE
               VVIIICJJEE
               MIIIIIJJEE
               MIIISIJEEE
               MMMISSJEEE"""


@pytest.mark.parametrize(
    ("garden_str", "expected_checksum"),
    [(_garden_a, 140), (_garden_b, 772), (_garden_c, 1930)],
)
def test_garden_iterates_through_all_regions(garden_str, expected_checksum):
    garden = Garden(CharacterGrid(garden_str))
    checksum = sum(r.area * r.perimeter for r in garden.regions())
    assert expected_checksum == checksum
