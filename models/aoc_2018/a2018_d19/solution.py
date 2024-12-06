from math import sqrt
from typing import Iterator

from models.aoc_2018.three_value_instructions import parse_three_value_instructions
from models.common.assembly import Computer, ImmutableProgram, Processor
from models.common.io import IOHandler, Problem, ProblemSolution


def optimized_sum_divisors_program(a: int, b: int) -> int:
    n_part_1 = 22 * a + b + 836
    n = n_part_1 + 10550400

    sqrt_n = int(sqrt(n))
    return sum(d + n // d for d in range(1, sqrt_n + 1) if n % d == 0) - sqrt_n * (
        sqrt_n * sqrt_n == n
    )


def aoc_2018_d19(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2018, 19, "Go With The Flow")
    io_handler.output_writer.write_header(problem_id)
    instructions = list(parse_three_value_instructions(io_handler.input_reader))
    program = ImmutableProgram(instructions)
    computer = Computer.from_processor(Processor())
    io_handler.output_writer.give_time_estimation("30s", part=1)
    computer.run_program(program)
    result = computer.get_register_value(register=0)
    yield ProblemSolution(
        problem_id,
        f"Value of register 0 at the end of the program: {result}",
        result,
        part=1,
    )

    # Part 2 was optimized by hand
    result = optimized_sum_divisors_program(
        a=instructions[21]._input_b.value,
        b=instructions[23]._input_b.value,
    )
    yield ProblemSolution(
        problem_id,
        f"Value of register 0 at the end of the program: {result}",
        result,
        part=2,
    )
