from io import StringIO
import numpy as np
from models.common.io import IOHandler, Problem, ProblemSolution
from .spreadsheet import Spreadsheet


def aoc_2017_d2(io_handler: IOHandler) -> None:
    problem_id = Problem(2017, 2, "Corruption Checksum")
    io_handler.output_writer.write_header(problem_id)
    string_io = StringIO(io_handler.input_reader.read())
    spreadsheet = Spreadsheet(np.loadtxt(string_io, dtype=int, delimiter="\t"))
    solution = ProblemSolution(
        problem_id,
        f"Spreadsheet checksum min/max: {spreadsheet.checksum_min_max()}",
        part=1,
    )
    io_handler.output_writer.write_solution(solution)
    solution = ProblemSolution(
        problem_id,
        f"Spreadsheet checksum divisibility: {spreadsheet.checksum_divisibility()}",
        part=2,
    )
    io_handler.output_writer.write_solution(solution)
