from enum import Enum


class HexDirection(str, Enum):
    NORTH = "n"
    NORTHEAST = "ne"
    NORTHWEST = "nw"
    SOUTH = "s"
    SOUTHEAST = "se"
    SOUTHWEST = "sw"


def num_hex_steps_away(directions: list[HexDirection]) -> int:
    steps = {HexDirection.NORTH: 0, HexDirection.NORTHEAST: 0}
    for direction in directions:
        if direction == HexDirection.NORTH:
            steps[HexDirection.NORTH] += 1
        elif direction == HexDirection.NORTHEAST:
            steps[HexDirection.NORTHEAST] += 1
        elif direction == HexDirection.SOUTH:
            steps[HexDirection.NORTH] -= 1
        elif direction == HexDirection.SOUTHWEST:
            steps[HexDirection.NORTHEAST] -= 1
        elif direction == HexDirection.NORTHWEST:
            steps[HexDirection.NORTH] += 1
            steps[HexDirection.NORTHEAST] -= 1
        elif direction == HexDirection.SOUTHEAST:
            steps[HexDirection.NORTH] -= 1
            steps[HexDirection.NORTHEAST] += 1
    steps_north = steps[HexDirection.NORTH]
    steps_northeast = steps[HexDirection.NORTHEAST]
    if steps_north * steps_northeast >= 0:
        return abs(steps_north) + abs(steps_northeast)
    else:
        return max(abs(steps_north), abs(steps_northeast))
