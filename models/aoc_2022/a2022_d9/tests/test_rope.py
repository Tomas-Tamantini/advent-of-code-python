from models.common.vectors import Vector2D, CardinalDirection
from ..rope import Rope


def test_rope_tail_position_is_head_minus_offset():
    rope = Rope(head=Vector2D(10, 20), tail_to_head=Vector2D(4, 7))
    assert rope.tail == Vector2D(6, 13)


def test_moving_head_does_not_affect_tail_if_they_remain_adjacent():
    rope = Rope(head=Vector2D(10, 20), tail_to_head=Vector2D(1, 0))
    new_rope = rope.move_head(CardinalDirection.NORTH)
    assert new_rope.head == Vector2D(10, 21)
    assert new_rope.tail == rope.tail


def test_moving_head_away_from_tail_in_aligned_position_brings_tail_along():
    rope = Rope(head=Vector2D(1, 0), tail_to_head=Vector2D(1, 0))
    new_rope = rope.move_head(CardinalDirection.EAST)
    assert new_rope.head == Vector2D(2, 0)
    assert new_rope.tail == Vector2D(1, 0)


def test_moving_head_away_from_tail_in_diagonal_position_brings_tail_along():
    rope = Rope(head=Vector2D(-1, -1), tail_to_head=Vector2D(-1, -1))
    new_rope = rope.move_head(CardinalDirection.SOUTH)
    assert new_rope.head == Vector2D(-1, -2)
    assert new_rope.tail == Vector2D(-1, -1)
