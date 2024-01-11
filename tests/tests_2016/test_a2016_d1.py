from models.aoc_2016 import TurnDirection, TurtleInstruction, Turtle
from models.vectors import CardinalDirection, Vector2D


def test_turtle_starts_at_origin():
    turtle = Turtle(initial_direction=CardinalDirection.NORTH)
    assert turtle.position == Vector2D(0, 0)


def test_turtle_can_follow_instruction():
    turtle = Turtle(initial_direction=CardinalDirection.NORTH)
    turtle.move(TurtleInstruction(TurnDirection.RIGHT, 2))
    assert turtle.position == Vector2D(2, 0)
    assert turtle.direction == CardinalDirection.EAST


def test_turtle_keeps_history_of_all_lattice_points_visited():
    turtle = Turtle(initial_direction=CardinalDirection.NORTH)
    turtle.move(TurtleInstruction(TurnDirection.RIGHT, 2))
    assert turtle.path_history == [Vector2D(0, 0), Vector2D(1, 0), Vector2D(2, 0)]


def test_can_iterate_through_points_where_turtle_path_crosses_itself():
    turtle = Turtle(initial_direction=CardinalDirection.NORTH)
    turtle.move(TurtleInstruction(TurnDirection.RIGHT, 8))
    turtle.move(TurtleInstruction(TurnDirection.RIGHT, 4))
    turtle.move(TurtleInstruction(TurnDirection.RIGHT, 4))
    turtle.move(TurtleInstruction(TurnDirection.RIGHT, 8))
    assert list(turtle.path_self_intersections()) == [Vector2D(4, 0)]
