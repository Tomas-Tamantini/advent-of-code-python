from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_cuboid_instructions
from .reactor_cells import num_reactor_cells_on


def aoc_2021_d22(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2021, 22, "Reactor Reboot")
    io_handler.output_writer.write_header(problem_id)
    instructions = list(parse_cuboid_instructions(io_handler.input_reader))
    small_instructions = [
        instruction
        for instruction in instructions
        if instruction.cuboid.all_coords_are_between(-50, 50)
    ]
    result = num_reactor_cells_on(small_instructions)
    yield ProblemSolution(
        problem_id,
        f"The number of cells turned on in smaller volume is {result}",
        result,
        part=1,
    )

    result = num_reactor_cells_on(instructions)
    yield ProblemSolution(
        problem_id,
        f"The number of cells turned on in entire volume is {result}",
        result,
        part=2,
    )
