from models.common.vectors import Vector2D, CardinalDirection
from models.common.io import IOHandler
from .parser import parse_navigation_instructions
from .ship import Ship


def aoc_2020_d12(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2020, 12, "Rain Risk")
    ship_instructions = parse_navigation_instructions(io_handler.input_reader)
    ship = Ship(position=Vector2D(0, 0), facing=CardinalDirection.EAST)
    for instruction in ship_instructions:
        ship = instruction.execute(ship)
    manhattan_distance = ship.position.manhattan_size
    print(f"Part 1: Ship's manhattan distance: {manhattan_distance}")

    waypoint_instructions = parse_navigation_instructions(
        io_handler.input_reader, relative_to_waypoint=True
    )
    ship = Ship(
        position=Vector2D(0, 0), facing=CardinalDirection.EAST, waypoint=Vector2D(10, 1)
    )
    for instruction in waypoint_instructions:
        ship = instruction.execute(ship)
    manhattan_distance = ship.position.manhattan_size
    print(f"Part 2: Ship's manhattan distance with waypoint: {manhattan_distance}")
