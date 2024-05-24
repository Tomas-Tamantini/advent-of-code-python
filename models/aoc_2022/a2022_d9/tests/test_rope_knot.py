import pytest
from models.common.vectors import Vector2D, CardinalDirection
from ..logic import RopeKnot


def test_rope_knot_can_be_moved_in_any_direction():
    knot = RopeKnot(Vector2D(10, 20))
    new_knot = knot.move(CardinalDirection.NORTH)
    assert new_knot.position == Vector2D(10, 21)


@pytest.mark.parametrize("tail_position", [(0, 0), (1, 0), (-1, -1)])
def test_rope_knot_does_not_pull_knots_adjacent_to_itself(tail_position):
    head_knot = RopeKnot(position=Vector2D(0, 0))
    tail_knot = RopeKnot(position=Vector2D(*tail_position))
    assert head_knot.pull(tail_knot) == tail_knot


@pytest.mark.parametrize(
    "old_tail_position, new_tail_position",
    [((10, 22), (10, 21)), ((8, 20), (9, 20))],
)
def test_rope_knots_aligned_with_head_but_two_units_away_get_pulled_one_unit(
    old_tail_position, new_tail_position
):
    head_knot = RopeKnot(position=Vector2D(10, 20))
    tail_knot = RopeKnot(position=Vector2D(*old_tail_position))
    new_tail_knot = head_knot.pull(tail_knot)
    assert new_tail_knot.position == Vector2D(*new_tail_position)


@pytest.mark.parametrize(
    "old_tail_position, new_tail_position",
    [((11, 22), (10, 21)), ((12, 18), (11, 19))],
)
def test_rope_knots_not_aligned_with_head_two_units_away_get_pulled_one_unit_in_each_coordinate(
    old_tail_position, new_tail_position
):
    head_knot = RopeKnot(position=Vector2D(10, 20))
    tail_knot = RopeKnot(position=Vector2D(*old_tail_position))
    new_tail_knot = head_knot.pull(tail_knot)
    assert new_tail_knot.position == Vector2D(*new_tail_position)
