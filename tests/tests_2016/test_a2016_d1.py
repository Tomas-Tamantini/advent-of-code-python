from models.aoc_2016 import TurnDirection, turtle_destination, TurtleInstruction
from models.vectors import CardinalDirection, Vector2D


def test_turtle_without_instructions_ends_up_at_origin():
    assert turtle_destination([]) == Vector2D(0, 0)


def test_turtle_properly_follows_instructions():
    instructions = [
        TurtleInstruction(TurnDirection.RIGHT, 2),
        TurtleInstruction(TurnDirection.LEFT, 3),
    ]
    assert turtle_destination(
        instructions, initial_direction=CardinalDirection.NORTH
    ) == Vector2D(2, 3)
