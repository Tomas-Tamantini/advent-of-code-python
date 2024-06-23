from io import StringIO
import numpy as np
from models.common.io import IOHandler, Problem
from .spreadsheet import Spreadsheet


def aoc_2017_d2(io_handler: IOHandler) -> None:
    problem_id = Problem(2017, 2, "Corruption Checksum")
    io_handler.output_writer.write_header(problem_id)
    string_io = StringIO(io_handler.input_reader.read())
    spreadsheet = Spreadsheet(np.loadtxt(string_io, dtype=int, delimiter="\t"))
    print(f"Part 1: Spreadsheet checksum min/max: {spreadsheet.checksum_min_max()}")
    print(
        f"Part 2: Spreadsheet checksum divisibility: {spreadsheet.checksum_divisibility()}"
    )
