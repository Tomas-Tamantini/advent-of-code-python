from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from models.aoc_2017.a2017_d18.parser import parse_duet_code
from .coprocessor import (
    count_multiply_instructions,
    optimized_coprocessor_code,
    SpyMultiplyInstruction,
)


def aoc_2017_d23(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 23, "Coprocessor Conflagration")
    io_handler.output_writer.write_header(problem_id)
    instructions = list(
        parse_duet_code(io_handler.input_reader, mul_cls=SpyMultiplyInstruction)
    )
    num_multiply_instructions = count_multiply_instructions(instructions)
    yield ProblemSolution(
        problem_id,
        f"Number of multiply instructions: {num_multiply_instructions}",
        part=1,
        result=num_multiply_instructions,
    )

    h_register = optimized_coprocessor_code(
        initial_a=1, initial_b=instructions[0].source
    )
    yield ProblemSolution(
        problem_id, f"Value of register h: {h_register}", part=2, result=h_register
    )
