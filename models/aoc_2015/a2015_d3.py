from models.vectors import CardinalDirection, Vector2D


def houses_with_at_least_one_present(instructions: str) -> set[tuple[int, int]]:
    directions = {
        "^": CardinalDirection.NORTH,
        ">": CardinalDirection.EAST,
        "v": CardinalDirection.SOUTH,
        "<": CardinalDirection.WEST,
    }
    current_position = Vector2D(0, 0)
    visited_houses = {current_position}
    for instruction in instructions:
        current_position = current_position.move(directions[instruction])
        visited_houses.add(current_position)
    return visited_houses
