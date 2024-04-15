from models.vectors import Vector2D, CardinalDirection, TurnDirection
from models.aoc_2020 import (
    Ship,
    MoveShipInstruction,
    MoveShipForwardInstruction,
    TurnShipInstruction,
)


def test_ship_moves_in_given_direction_without_changing_orientation():
    ship = Ship(position=Vector2D(0, 0), facing=CardinalDirection.EAST)
    move = MoveShipInstruction(direction=CardinalDirection.NORTH, distance=10)
    new_ship = move.execute(ship)
    assert new_ship == Ship(position=Vector2D(0, 10), facing=CardinalDirection.EAST)


def test_ship_moves_forward_given_number_of_steps():
    ship = Ship(position=Vector2D(0, 0), facing=CardinalDirection.WEST)
    move = MoveShipForwardInstruction(distance=13)
    new_ship = move.execute(ship)
    assert new_ship == Ship(position=Vector2D(-13, 0), facing=CardinalDirection.WEST)


def test_ship_turns_without_changing_position():
    ship = Ship(position=Vector2D(0, 0), facing=CardinalDirection.EAST)
    move = TurnShipInstruction(turn_direction=TurnDirection.RIGHT)
    new_ship = move.execute(ship)
    assert new_ship == Ship(position=Vector2D(0, 0), facing=CardinalDirection.SOUTH)
