import pytest

from models.common.io import CharacterGrid

from .logic import Garden

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

_garden_d = """EEEEE
               EXXXX
               EEEEE
               EXXXX
               EEEEE"""

_garden_e = """AAAAAA
               AAABBA
               AAABBA
               ABBAAA
               ABBAAA
               AAAAAA"""


@pytest.mark.parametrize(
    ("garden_str", "perimeter_checksum", "sides_checksum"),
    [
        (_garden_a, 140, 80),
        (_garden_b, 772, 436),
        (_garden_c, 1930, 1206),
        (_garden_d, 692, 236),
        (_garden_e, 1184, 368),
    ],
)
def test_garden_iterates_through_all_regions(
    garden_str, perimeter_checksum, sides_checksum
):
    garden = Garden(CharacterGrid(garden_str))
    dimensions = [r.dimensions() for r in garden.regions()]
    actual_perimeter_checksum = sum(r.area * r.perimeter for r in dimensions)
    assert perimeter_checksum == actual_perimeter_checksum

    actual_sides_checksum = sum(r.area * r.num_sides for r in dimensions)
    assert sides_checksum == actual_sides_checksum
