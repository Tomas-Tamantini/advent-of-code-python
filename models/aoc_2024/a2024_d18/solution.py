from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D
from math import log2, ceil
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

    # TODO: Extract method
    lb = 1024
    ub = len(corrupted_positions)
    expected_num_steps = ceil(log2(ub - lb))
    while lb < ub:
        mid = (lb + ub) // 2
        remaining_steps = ceil(log2(ub - lb))
        io_handler.progress_bar.update(
            expected_num_steps - remaining_steps, expected_num_steps
        )
        memory = Memory2D(
            width=71, height=71, corrupted_positions=corrupted_positions[:mid]
        )
        if memory.shortest_path(Vector2D(0, 0), Vector2D(70, 70)) != -1:
            lb = mid + 1
        else:
            ub = mid

    coords = corrupted_positions[lb - 1]
    result = f"{coords.x},{coords.y}"

    yield ProblemSolution(
        problem_id,
        f"The first corrupted position that blocks the path is {result}",
        result,
        part=2,
    )
