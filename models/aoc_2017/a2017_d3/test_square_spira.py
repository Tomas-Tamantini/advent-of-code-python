import pytest
from models.common.vectors import Vector2D
from .square_spiral import SquareSpiral


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
    assert SquareSpiral.coordinates(index) == Vector2D(*coordinates)
    assert SquareSpiral.spiral_index(*coordinates) == index


def test_can_generate_sequence_of_numbers_equal_to_sum_of_adjacent_ones():
    sequence = SquareSpiral.adjacent_sum_sequence()
    first_terms = [next(sequence) for _ in range(10)]
    assert first_terms == [1, 1, 2, 4, 5, 10, 11, 23, 25, 26]
