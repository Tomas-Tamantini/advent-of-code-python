from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from models.aoc_2016.assembunny import (
    parse_assembunny_code,
)
from .clock_signal import smallest_value_to_send_clock_signal


def aoc_2016_d25(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2016, 25, "Clock Signal")
    io_handler.output_writer.write_header(problem_id)
    program = parse_assembunny_code(io_handler.input_reader)
    smallest_value = smallest_value_to_send_clock_signal(program)
    yield ProblemSolution(
        problem_id,
        f"Smallest value to send clock signal: {smallest_value}",
        result=smallest_value,
    )
