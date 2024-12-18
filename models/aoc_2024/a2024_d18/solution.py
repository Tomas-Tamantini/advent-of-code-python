from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D

from .memory_2d import Memory2D
from .parser import parse_byte_positions


def aoc_2024_d18(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 18, "RAM Run")
    io_handler.output_writer.write_header(problem_id)
    corrupted_positions = list(parse_byte_positions(io_handler.input_reader))

    memory = Memory2D(
        width=71, height=71, corrupted_positions=corrupted_positions[:1024]
    )
    min_steps = memory.shortest_path(Vector2D(0, 0), Vector2D(70, 70))
    yield ProblemSolution(
        problem_id,
        f"The minimum number of steps to reach the end of memory is {min_steps}",
        result=min_steps,
        part=1,
    )
