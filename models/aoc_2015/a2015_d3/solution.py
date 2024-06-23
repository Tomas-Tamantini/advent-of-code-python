from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import CardinalDirection, Vector2D


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


def aoc_2015_d3(io_handler: IOHandler) -> None:
    problem_id = Problem(2015, 3, "Perfectly Spherical Houses in a Vacuum")
    io_handler.output_writer.write_header(problem_id)
    instructions = io_handler.input_reader.read()

    houses = houses_with_at_least_one_present(instructions)
    solution = ProblemSolution(
        problem_id, f"Santa visits {len(houses)} houses", part=1, result=len(houses)
    )
    io_handler.set_solution(solution)

    houses_santa = houses_with_at_least_one_present(instructions[::2])
    houses_robot = houses_with_at_least_one_present(instructions[1::2])
    houses = houses_santa.union(houses_robot)
    solution = ProblemSolution(
        problem_id,
        f"Santa and Robot Santa visit {len(houses)} houses",
        part=2,
        result=len(houses),
    )
    io_handler.set_solution(solution)
