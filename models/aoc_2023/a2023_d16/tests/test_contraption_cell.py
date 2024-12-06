import pytest

from models.common.vectors import CardinalDirection

from ..logic import EmptyCell, Mirror, Splitter


def test_empty_contraption_cell_does_not_change_beam_direction():
    cell = EmptyCell()
    new_directions = list(cell.next_directions(CardinalDirection.EAST))
    assert new_directions == [CardinalDirection.EAST]


@pytest.mark.parametrize(
    ("is_upward_diagonal", "incoming_direction", "reflected_direction"),
    [
        (True, CardinalDirection.EAST, CardinalDirection.NORTH),
        (True, CardinalDirection.NORTH, CardinalDirection.EAST),
        (True, CardinalDirection.WEST, CardinalDirection.SOUTH),
        (True, CardinalDirection.SOUTH, CardinalDirection.WEST),
        (False, CardinalDirection.EAST, CardinalDirection.SOUTH),
        (False, CardinalDirection.NORTH, CardinalDirection.WEST),
        (False, CardinalDirection.WEST, CardinalDirection.NORTH),
        (False, CardinalDirection.SOUTH, CardinalDirection.EAST),
    ],
)
def test_mirror_reflects_beam_by_90_degrees(
    is_upward_diagonal, incoming_direction, reflected_direction
):
    mirror = Mirror(is_upward_diagonal)
    new_directions = list(mirror.next_directions(incoming_direction))
    assert new_directions == [reflected_direction]


@pytest.mark.parametrize(
    ("is_horizontal", "direction"),
    [
        (True, CardinalDirection.EAST),
        (True, CardinalDirection.WEST),
        (False, CardinalDirection.NORTH),
        (False, CardinalDirection.SOUTH),
    ],
)
def test_beam_parallel_to_splitter_continues_in_same_direction(
    is_horizontal, direction
):
    splitter = Splitter(is_horizontal)
    new_directions = list(splitter.next_directions(direction))
    assert new_directions == [direction]


@pytest.mark.parametrize(
    ("is_horizontal", "direction"),
    [
        (True, CardinalDirection.NORTH),
        (True, CardinalDirection.SOUTH),
        (False, CardinalDirection.EAST),
        (False, CardinalDirection.WEST),
    ],
)
def test_beam_perpendicular_to_splitter_gets_split_in_two_directions(
    is_horizontal, direction
):
    splitter = Splitter(is_horizontal)
    new_directions = list(splitter.next_directions(direction))
    assert len(new_directions) == 2
    assert set(new_directions) == {direction.turn_left(), direction.turn_right()}
