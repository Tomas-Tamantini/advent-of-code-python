from models.common.vectors import Vector2D, CardinalDirection
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_navigation_instructions
from .ship import Ship


def aoc_2020_d12(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 12, "Rain Risk")
    io_handler.output_writer.write_header(problem_id)
    ship_instructions = parse_navigation_instructions(io_handler.input_reader)
    ship = Ship(position=Vector2D(0, 0), facing=CardinalDirection.EAST)
    for instruction in ship_instructions:
        ship = instruction.execute(ship)
    manhattan_distance = ship.position.manhattan_size
    solution = ProblemSolution(
        problem_id, f"Ship's manhattan distance: {manhattan_distance}", part=1
    )
    io_handler.output_writer.write_solution(solution)

    waypoint_instructions = parse_navigation_instructions(
        io_handler.input_reader, relative_to_waypoint=True
    )
    ship = Ship(
        position=Vector2D(0, 0), facing=CardinalDirection.EAST, waypoint=Vector2D(10, 1)
    )
    for instruction in waypoint_instructions:
        ship = instruction.execute(ship)
    manhattan_distance = ship.position.manhattan_size
    solution = ProblemSolution(
        problem_id,
        f"Ship's manhattan distance with waypoint: {manhattan_distance}",
        part=2,
    )
    io_handler.output_writer.write_solution(solution)
