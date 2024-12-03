from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .logic import parse_program, StackWithConditional, StackWithoutConditional


def aoc_2024_d3(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 3, "Mull It Over")
    io_handler.output_writer.write_header(problem_id)
    program = io_handler.input_reader.read().strip()
    instructions = list(parse_program(program))
    stack_without_conditional = StackWithoutConditional()
    for instruction in instructions:
        instruction.execute(stack_without_conditional)
    total = stack_without_conditional.result
    yield ProblemSolution(
        problem_id,
        f"The total of all multiplications in the program is {total}",
        result=total,
        part=1,
    )

    stack_with_conditional = StackWithConditional()
    for instruction in instructions:
        instruction.execute(stack_with_conditional)
    total = stack_with_conditional.result
    yield ProblemSolution(
        problem_id,
        f"The total of multiplications within enabled blocks is {total}",
        result=total,
        part=2,
    )
