from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import fragmented_checksum, integral_checksum
from .parser import parse_disk_files


def aoc_2024_d9(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 9, "Disk Fragmenter")
    io_handler.output_writer.write_header(problem_id)
    files = set(parse_disk_files(io_handler.input_reader))
    fragmented = fragmented_checksum(files)
    yield ProblemSolution(
        problem_id,
        f"The fragmented checksum is {fragmented}",
        result=fragmented,
        part=1,
    )

    integral = integral_checksum(files)
    yield ProblemSolution(
        problem_id,
        f"The integral checksum is {integral}",
        result=integral,
        part=2,
    )
