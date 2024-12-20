from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .conditional_increment import maximum_value_at_registers
from .parser import parse_conditional_increment_instructions


def aoc_2017_d8(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 8, "I Heard You Like Registers")
    io_handler.output_writer.write_header(problem_id)
    instructions = list(
        parse_conditional_increment_instructions(io_handler.input_reader)
    )
    max_values = list(maximum_value_at_registers(instructions))
    max_value_final = max_values[-1]
    max_value_all_time = max(max_values)
    yield ProblemSolution(
        problem_id,
        f"Maximum register value at end: {max_value_final}",
        part=1,
        result=max_value_final,
    )

    yield ProblemSolution(
        problem_id,
        f"Maximum register value at any time: {max_value_all_time}",
        part=2,
        result=max_value_all_time,
    )
