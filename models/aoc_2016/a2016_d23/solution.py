from models.common.io import IOHandler, Problem, ProblemSolution
from models.aoc_2016.assembunny import parse_assembunny_code, run_self_referential_code


def aoc_2016_d23(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 23, "Safe Cracking")
    io_handler.output_writer.write_header(problem_id)
    program = parse_assembunny_code(io_handler.input_reader)
    a7 = run_self_referential_code(program, initial_value=7)
    solution = ProblemSolution(
        problem_id, f"Value in register a if a starts as 7: {a7}", part=1
    )
    io_handler.output_writer.write_solution(solution)
    a12 = run_self_referential_code(program, initial_value=12)
    solution = ProblemSolution(
        problem_id, f"Value in register a if a starts as 12: {a12}", part=2
    )
    io_handler.output_writer.write_solution(solution)
