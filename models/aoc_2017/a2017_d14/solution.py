from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .disk_grid import DiskGrid


def aoc_2017_d14(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 14, "Disk Defragmentation")
    io_handler.output_writer.write_header(problem_id)
    key = io_handler.input_reader.read().strip()
    num_rows = 128
    grid = DiskGrid(key, num_rows)
    yield ProblemSolution(
        problem_id, f"Number of used squares: {grid.num_used_squares()}", part=1
    )

    yield ProblemSolution(
        problem_id, f"Number of regions: {grid.num_regions()}", part=2
    )
