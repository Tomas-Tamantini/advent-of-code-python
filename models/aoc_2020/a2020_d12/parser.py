from typing import Iterator

from models.common.io import InputReader
from models.common.vectors import CardinalDirection, TurnDirection

from .ship import (
    MoveShipForwardInstruction,
    MoveShipInstruction,
    MoveTowardsWaypointInstruction,
    MoveWaypointInstruction,
    NavigationInstruction,
    RotateWaypointInstruction,
    TurnShipInstruction,
)


def _parse_navigation_instruction(
    instruction: str, relative_to_waypoint: bool
) -> NavigationInstruction:
    action = instruction[0]
    value = int(instruction[1:])
    directions = {
        "N": CardinalDirection.NORTH,
        "S": CardinalDirection.SOUTH,
        "E": CardinalDirection.EAST,
        "W": CardinalDirection.WEST,
    }
    if action == "F":
        return (
            MoveTowardsWaypointInstruction(value)
            if relative_to_waypoint
            else MoveShipForwardInstruction(value)
        )
    elif action in directions:
        return (
            MoveWaypointInstruction(directions[action], value)
            if relative_to_waypoint
            else MoveShipInstruction(directions[action], value)
        )
    elif action in {"L", "R"}:
        if value == 0:
            turn = TurnDirection.NO_TURN
        elif value == 90:
            turn = TurnDirection.LEFT if action == "L" else TurnDirection.RIGHT
        elif value == 180:
            turn = TurnDirection.U_TURN
        elif value == 270:
            turn = TurnDirection.RIGHT if action == "L" else TurnDirection.LEFT
        else:
            raise ValueError(f"Invalid turn angle: {value}")
        return (
            RotateWaypointInstruction(turn)
            if relative_to_waypoint
            else TurnShipInstruction(turn)
        )
    else:
        raise ValueError(f"Unknown navigation instruction: {instruction}")


def parse_navigation_instructions(
    input_reader: InputReader, relative_to_waypoint: bool = False
) -> Iterator[NavigationInstruction]:
    for line in input_reader.read_stripped_lines():
        yield _parse_navigation_instruction(line, relative_to_waypoint)
