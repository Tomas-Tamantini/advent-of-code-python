from models.common.io import IOHandler
from models.aoc_2017.a2017_d18.parser import parse_duet_code
from .coprocessor import (
    count_multiply_instructions,
    optimized_coprocessor_code,
    SpyMultiplyInstruction,
)


def aoc_2017_d23(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2017, 23, "Coprocessor Conflagration")
    instructions = list(
        parse_duet_code(io_handler.input_reader, mul_cls=SpyMultiplyInstruction)
    )
    num_multiply_instructions = count_multiply_instructions(instructions)
    print(f"Part 1: Number of multiply instructions: {num_multiply_instructions}")
    h_register = optimized_coprocessor_code(
        initial_a=1, initial_b=instructions[0].source
    )
    print(f"Part 2: Value of register h: {h_register}")
