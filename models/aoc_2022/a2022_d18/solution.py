from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_cube_positions
from .logic import total_surface_area, external_surface_area


def aoc_2022_d18(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2022, 18, "Boiling Boulders")
    io_handler.output_writer.write_header(problem_id)
    cubes = set(parse_cube_positions(io_handler.input_reader))
    total_area = total_surface_area(cubes)
    yield ProblemSolution(
        problem_id, f"Total surface area of droplet is {total_area}", part=1
    )

    external_area = external_surface_area(cubes)
    yield ProblemSolution(
        problem_id, f"External surface area of droplet is {external_area}", part=2
    )
