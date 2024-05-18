from models.common.vectors import Vector2D, CardinalDirection, TurnDirection
from models.aoc_2020 import (
    Ship,
    MoveShipInstruction,
    MoveShipForwardInstruction,
    TurnShipInstruction,
    MoveTowardsWaypointInstruction,
    MoveWaypointInstruction,
    RotateWaypointInstruction,
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


def test_ship_moves_towards_waypoint_given_number_of_times():
    ship = Ship(
        position=Vector2D(0, 0), facing=CardinalDirection.EAST, waypoint=Vector2D(10, 3)
    )
    move = MoveTowardsWaypointInstruction(times=2)
    new_ship = move.execute(ship)
    assert new_ship == Ship(
        position=Vector2D(20, 6),
        facing=CardinalDirection.EAST,
        waypoint=Vector2D(10, 3),
    )


def test_waypoint_moves_in_given_direction():
    ship = Ship(
        position=Vector2D(0, 0), facing=CardinalDirection.EAST, waypoint=Vector2D(10, 3)
    )
    move = MoveWaypointInstruction(direction=CardinalDirection.NORTH, distance=4)
    new_ship = move.execute(ship)
    assert new_ship == Ship(
        position=Vector2D(0, 0), facing=CardinalDirection.EAST, waypoint=Vector2D(10, 7)
    )


def test_waypoint_rotates_right_around_ship():
    ship = Ship(
        position=Vector2D(1, 1), facing=CardinalDirection.EAST, waypoint=Vector2D(10, 3)
    )
    move = RotateWaypointInstruction(turn_direction=TurnDirection.RIGHT)
    new_ship = move.execute(ship)
    assert new_ship == Ship(
        position=Vector2D(1, 1),
        facing=CardinalDirection.EAST,
        waypoint=Vector2D(3, -10),
    )


def test_waypoint_rotates_left_around_ship():
    ship = Ship(
        position=Vector2D(1, 1), facing=CardinalDirection.EAST, waypoint=Vector2D(10, 3)
    )
    move = RotateWaypointInstruction(turn_direction=TurnDirection.LEFT)
    new_ship = move.execute(ship)
    assert new_ship == Ship(
        position=Vector2D(1, 1),
        facing=CardinalDirection.EAST,
        waypoint=Vector2D(-3, 10),
    )


def test_waypoint_rotates_180_around_ship():
    ship = Ship(
        position=Vector2D(1, 1), facing=CardinalDirection.EAST, waypoint=Vector2D(10, 3)
    )
    move = RotateWaypointInstruction(turn_direction=TurnDirection.U_TURN)
    new_ship = move.execute(ship)
    assert new_ship == Ship(
        position=Vector2D(1, 1),
        facing=CardinalDirection.EAST,
        waypoint=Vector2D(-10, -3),
    )
