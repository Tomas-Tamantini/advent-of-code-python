from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution


def _calculate_a(a: int, b: int) -> int:
    new_a = a + (b & 0xFF)
    new_a &= 0xFFFFFF
    new_a *= 65899
    new_a &= 0xFFFFFF
    return new_a


def optimized_simple_conversion(input_num: int) -> int:
    a = 0
    while True:
        b = a | 0x10000
        a = input_num
        while True:
            a = _calculate_a(a, b)
            if b < 256:
                return a
            b //= 256


def optimized_complex_conversion(input_num: int) -> int:
    visited = set()
    max_num_attempts = 1000
    a = 0
    last_a = -1
    while True:
        b = a | 0x10000
        a = input_num
        while True:
            a = _calculate_a(a, b)
            if b < 256:
                if a not in visited:
                    visited.add(a)
                    last_a = a
                    max_num_attempts = 1000
                else:
                    max_num_attempts -= 1
                    if max_num_attempts == 0:
                        return last_a
                break
            b //= 256


def aoc_2018_d21(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2018, 21, "Chronal Conversion")
    io_handler.output_writer.write_header(problem_id)
    lines = list(io_handler.input_reader.readlines())
    input_number = int(lines[8].split()[1])
    register_min = optimized_simple_conversion(input_number)
    yield ProblemSolution(
        problem_id,
        f"Value of register 0 to halt program with min instructions: {register_min}",
        part=1,
        result=register_min,
    )

    register_max = optimized_complex_conversion(input_number)
    yield ProblemSolution(
        problem_id,
        f"Value of register 0 to halt program with max instructions: {register_max}",
        part=2,
        result=register_max,
    )
