from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from .parser import parse_patrol_area, parse_patrol_guard
from .logic import patrol_route


def aoc_2024_d6(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 6, "Guard Gallivant")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    area = parse_patrol_area(grid)
    guard = parse_patrol_guard(grid)
    num_positions = len(set(patrol_route(area, guard)))
    yield ProblemSolution(
        problem_id,
        f"The number of unique positions visited by the guard is {num_positions}",
        result=num_positions,
        part=1,
    )
