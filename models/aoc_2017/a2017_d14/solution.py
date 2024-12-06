from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .disk_grid import DiskGrid


def aoc_2017_d14(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 14, "Disk Defragmentation")
    io_handler.output_writer.write_header(problem_id)
    key = io_handler.input_reader.read().strip()
    num_rows = 128
    grid = DiskGrid(key, num_rows)
    result = grid.num_used_squares()
    yield ProblemSolution(
        problem_id, f"Number of used squares: {result}", result, part=1
    )
    result = grid.num_regions()
    yield ProblemSolution(problem_id, f"Number of regions: {result}", result, part=2)
