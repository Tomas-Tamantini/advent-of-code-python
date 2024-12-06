from io import StringIO
from typing import Iterator

import numpy as np

from models.common.io import IOHandler, Problem, ProblemSolution

from .spreadsheet import Spreadsheet


def aoc_2017_d2(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 2, "Corruption Checksum")
    io_handler.output_writer.write_header(problem_id)
    string_io = StringIO(io_handler.input_reader.read())
    spreadsheet = Spreadsheet(np.loadtxt(string_io, dtype=int, delimiter="\t"))
    result = spreadsheet.checksum_min_max()
    yield ProblemSolution(
        problem_id, f"Spreadsheet checksum min/max: {result}", result, part=1
    )
    result = spreadsheet.checksum_divisibility()
    yield ProblemSolution(
        problem_id, f"Spreadsheet checksum divisibility: {result}", result, part=2
    )
