from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import Program3Bit, SerialOutput3Bit, run_3_bit_program
from .parser import parse_3_bit_program, parse_3_bit_registers


def aoc_2024_d17(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 17, "Chronospatial Computer")
    io_handler.output_writer.write_header(problem_id)

    instructions = parse_3_bit_program(io_handler.input_reader)
    registers = parse_3_bit_registers(io_handler.input_reader)

    program = Program3Bit(instructions)
    output = SerialOutput3Bit()
    run_3_bit_program(program, output, registers)
    result = output.get_output()

    yield ProblemSolution(
        problem_id, f"The output of the program is: {result}", result, part=1
    )
