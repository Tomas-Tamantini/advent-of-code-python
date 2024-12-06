from models.common.vectors import CardinalDirection, Vector2D

from ..logic import Rope


def test_rope_starts_with_all_knots_in_origin():
    rope = Rope(num_knots=3)
    positions = list(rope.positions_head_to_tail())
    assert positions == [Vector2D(0, 0) for _ in range(3)]


def test_pulling_on_rope_head_pulls_all_other_knots_along():
    rope = Rope(num_knots=3)
    tail_positions = [rope.tail_position]
    instructions = (
        CardinalDirection.EAST,
        CardinalDirection.EAST,
        CardinalDirection.NORTH,
        CardinalDirection.NORTH,
        CardinalDirection.NORTH,
        CardinalDirection.NORTH,
    )
    for instruction in instructions:
        rope.move_head(instruction)
        tail_positions.append(rope.tail_position)
    assert tail_positions == [
        Vector2D(x=0, y=0),
        Vector2D(x=0, y=0),
        Vector2D(x=0, y=0),
        Vector2D(x=0, y=0),
        Vector2D(x=1, y=1),
        Vector2D(x=1, y=1),
        Vector2D(x=2, y=2),
    ]
