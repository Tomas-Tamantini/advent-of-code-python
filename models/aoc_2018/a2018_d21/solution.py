from models.common.io import IOHandler, Problem, ProblemSolution


def optimized_chronal_conversion(input_num: int, exit_on_first_occurrence: bool) -> int:
    visited = set()
    max_num_attempts = 1000
    a = 0
    last_a = -1
    while True:
        b = a | 0x10000
        a = input_num
        while True:
            c = b & 0xFF
            a += c
            a &= 0xFFFFFF
            a *= 65899
            a &= 0xFFFFFF
            if 256 > b:
                if exit_on_first_occurrence:
                    return a
                else:
                    if a not in visited:
                        visited.add(a)
                        last_a = a
                        max_num_attempts = 1000
                    else:
                        max_num_attempts -= 1
                        if max_num_attempts == 0:
                            return last_a
                    break
            b = b // 256


def aoc_2018_d21(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 21, "Chronal Conversion")
    io_handler.output_writer.write_header(problem_id)
    lines = list(io_handler.input_reader.readlines())
    input_number = int(lines[8].split()[1])
    register_min = optimized_chronal_conversion(
        input_number, exit_on_first_occurrence=True
    )
    solution = ProblemSolution(
        problem_id,
        f"Value of register 0 to halt program with min instructions: {register_min}",
        part=1,
    )
    io_handler.output_writer.write_solution(solution)
    register_max = optimized_chronal_conversion(
        input_number, exit_on_first_occurrence=False
    )
    solution = ProblemSolution(
        problem_id,
        f"Value of register 0 to halt program with max instructions: {register_max}",
        part=2,
    )
    io_handler.output_writer.write_solution(solution)
