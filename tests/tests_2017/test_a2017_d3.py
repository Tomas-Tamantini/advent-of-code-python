import pytest
from models.aoc_2017 import SquareSpiral


@pytest.mark.parametrize(
    "index, coordinates",
    [
        (1, (0, 0)),
        (2, (1, 0)),
        (3, (1, 1)),
        (4, (0, 1)),
        (5, (-1, 1)),
        (6, (-1, 0)),
        (7, (-1, -1)),
        (8, (0, -1)),
        (9, (1, -1)),
        (59, (2, 4)),
        (72, (-4, -3)),
        (76, (-1, -4)),
        (82, (5, -4)),
        (91, (5, 5)),
        (92, (4, 5)),
        (101, (-5, 5)),
        (102, (-5, 4)),
        (111, (-5, -5)),
        (112, (-4, -5)),
        (121, (5, -5)),
        (312051, (-151, -279)),
    ],
)
def test_can_map_between_coordinates_and_spiral_indices(index, coordinates):
    assert SquareSpiral.coordinates(index) == coordinates
    assert SquareSpiral.spiral_index(*coordinates) == index
