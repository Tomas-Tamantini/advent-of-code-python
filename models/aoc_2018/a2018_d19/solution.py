from math import sqrt
from models.common.io import InputReader
from models.common.assembly import Processor, ImmutableProgram, Computer
from models.aoc_2018.three_value_instructions import parse_three_value_instructions


def optimized_sum_divisors_program(a: int, b: int) -> int:
    n_part_1 = 22 * a + b + 836
    n = n_part_1 + 10550400

    sqrt_n = int(sqrt(n))
    return sum(d + n // d for d in range(1, sqrt_n + 1) if n % d == 0) - sqrt_n * (
        sqrt_n * sqrt_n == n
    )


def aoc_2018_d19(input_reader: InputReader, **_) -> None:
    print("--- AOC 2018 - Day 19: Go With The Flow ---")
    instructions = list(parse_three_value_instructions(input_reader))
    program = ImmutableProgram(instructions)
    computer = Computer.from_processor(Processor())
    print("Part 1: Takes about 30s to run", end="\r")
    computer.run_program(program)
    value = computer.get_register_value(register=0)
    print(f"Part 1: Value of register 0 at the end of the program: {value}")
    # Part 2 was optimized by hand
    result = optimized_sum_divisors_program(
        a=instructions[21]._input_b.value,
        b=instructions[23]._input_b.value,
    )
    print(f"Part 2: Value of register 0 at the end of the program: {result}")
