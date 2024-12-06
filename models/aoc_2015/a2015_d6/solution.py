from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .light_grid import LightGrid
from .parser import parse_and_give_light_grid_instructions


def aoc_2015_d6(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2015, 6, "Probably a Fire Hazard")
    io_handler.output_writer.write_header(problem_id)
    grid = LightGrid(1000, 1000)
    parse_and_give_light_grid_instructions(io_handler.input_reader, grid)
    yield ProblemSolution(
        problem_id,
        f"There are {grid.num_lights_on} lights on",
        part=1,
        result=grid.num_lights_on,
    )

    grid = LightGrid(1000, 1000)
    parse_and_give_light_grid_instructions(
        io_handler.input_reader, grid, use_elvish_tongue=True
    )
    yield ProblemSolution(
        problem_id,
        f"The total brightness is {grid.total_brightness}",
        part=2,
        result=grid.total_brightness,
    )
