from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_bitmask_instructions
from .bitmask_memory import BitmaskMemory


def aoc_2020_d14(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 14, "Docking Data")
    io_handler.output_writer.write_header(problem_id)
    values_instructions = list(
        parse_bitmask_instructions(io_handler.input_reader, is_address_mask=False)
    )
    memory = BitmaskMemory()
    for instruction in values_instructions:
        instruction.execute(memory)
    solution = ProblemSolution(
        problem_id,
        f"Sum of values in memory after applying mask to values is {memory.sum_values()}",
        part=1,
    )
    io_handler.output_writer.write_solution(solution)

    address_instructions = list(
        parse_bitmask_instructions(io_handler.input_reader, is_address_mask=True)
    )
    memory = BitmaskMemory()
    for instruction in address_instructions:
        instruction.execute(memory)
    solution = ProblemSolution(
        problem_id,
        f"Sum of values in memory after applying mask to addresses is {memory.sum_values()}",
        part=2,
    )
    io_handler.output_writer.write_solution(solution)
