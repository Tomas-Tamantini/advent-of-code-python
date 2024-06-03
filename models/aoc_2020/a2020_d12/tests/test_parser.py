from models.common.io import InputFromString
from models.common.vectors import CardinalDirection, TurnDirection
from ..parser import parse_navigation_instructions
from ..ship import (
    MoveShipForwardInstruction,
    MoveShipInstruction,
    MoveTowardsWaypointInstruction,
    MoveWaypointInstruction,
    RotateWaypointInstruction,
    TurnShipInstruction,
)


def test_parse_navigation_instructions():
    file_content = """
                   F10
                   N3
                   F7
                   R90
                   R180
                   R270
                   R0
                   L90
                   """
    instructions = list(parse_navigation_instructions(InputFromString(file_content)))
    assert instructions == [
        MoveShipForwardInstruction(distance=10),
        MoveShipInstruction(direction=CardinalDirection.NORTH, distance=3),
        MoveShipForwardInstruction(distance=7),
        TurnShipInstruction(turn_direction=TurnDirection.RIGHT),
        TurnShipInstruction(turn_direction=TurnDirection.U_TURN),
        TurnShipInstruction(turn_direction=TurnDirection.LEFT),
        TurnShipInstruction(turn_direction=TurnDirection.NO_TURN),
        TurnShipInstruction(turn_direction=TurnDirection.LEFT),
    ]


def test_parse_navigation_instructions_for_waypoint():
    file_content = """
                   F10
                   N3
                   F7
                   R90
                   R180
                   R270
                   R0
                   L90
                   """
    instructions = list(
        parse_navigation_instructions(
            InputFromString(file_content), relative_to_waypoint=True
        )
    )
    assert instructions == [
        MoveTowardsWaypointInstruction(times=10),
        MoveWaypointInstruction(direction=CardinalDirection.NORTH, distance=3),
        MoveTowardsWaypointInstruction(times=7),
        RotateWaypointInstruction(turn_direction=TurnDirection.RIGHT),
        RotateWaypointInstruction(turn_direction=TurnDirection.U_TURN),
        RotateWaypointInstruction(turn_direction=TurnDirection.LEFT),
        RotateWaypointInstruction(turn_direction=TurnDirection.NO_TURN),
        RotateWaypointInstruction(turn_direction=TurnDirection.LEFT),
    ]
