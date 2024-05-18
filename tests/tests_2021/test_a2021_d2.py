from models.common.vectors import Vector2D, CardinalDirection
from models.aoc_2021 import (
    Submarine,
    MoveSubmarineInstruction,
    IncrementAimInstruction,
    MoveSubmarineWithAimInstruction,
)


def test_submarine_moves_in_given_direction_without_changing_aim():
    submarine = Submarine(position=Vector2D(0, 0), aim=123)
    move_down = MoveSubmarineInstruction(direction=CardinalDirection.SOUTH, distance=10)
    new_submarine = move_down.execute(submarine)
    assert new_submarine == Submarine(position=Vector2D(0, 10), aim=123)
    move_up = MoveSubmarineInstruction(direction=CardinalDirection.NORTH, distance=5)
    new_submarine = move_up.execute(new_submarine)
    assert new_submarine == Submarine(position=Vector2D(0, 5), aim=123)
    move_right = MoveSubmarineInstruction(direction=CardinalDirection.EAST, distance=3)
    new_submarine = move_right.execute(new_submarine)
    assert new_submarine == Submarine(position=Vector2D(3, 5), aim=123)


def test_submarine_aim_increments_by_given_amount():
    submarine = Submarine(aim=123)
    increment = IncrementAimInstruction(increment=10)
    new_submarine = increment.execute(submarine)
    assert new_submarine == Submarine(position=Vector2D(0, 0), aim=133)


def test_submarine_moves_forward_given_amount_and_down_according_to_aim():
    submarine = Submarine(position=Vector2D(10, 20), aim=13)
    move = MoveSubmarineWithAimInstruction(distance=12)
    new_submarine = move.execute(submarine)
    assert new_submarine == Submarine(position=Vector2D(22, 176), aim=13)
