from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .bitmask_memory import BitmaskMemory
from .parser import parse_bitmask_instructions


def aoc_2020_d14(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2020, 14, "Docking Data")
    io_handler.output_writer.write_header(problem_id)
    values_instructions = list(
        parse_bitmask_instructions(io_handler.input_reader, is_address_mask=False)
    )
    memory = BitmaskMemory()
    for instruction in values_instructions:
        instruction.execute(memory)
    result = memory.sum_values()
    yield ProblemSolution(
        problem_id,
        f"Sum of values in memory after applying mask to values is {result}",
        result,
        part=1,
    )

    address_instructions = list(
        parse_bitmask_instructions(io_handler.input_reader, is_address_mask=True)
    )
    memory = BitmaskMemory()
    for instruction in address_instructions:
        instruction.execute(memory)
    result = memory.sum_values()
    yield ProblemSolution(
        problem_id,
        f"Sum of values in memory after applying mask to addresses is {result}",
        result,
        part=2,
    )
