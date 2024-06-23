from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_password_policies_and_passwords


def aoc_2020_d2(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 2, "Password Philosophy")
    io_handler.output_writer.write_header(problem_id)
    num_valid_range_passwords = sum(
        1
        for policy, password in parse_password_policies_and_passwords(
            io_handler.input_reader, use_range_policy=True
        )
        if policy.is_valid(password)
    )
    solution = ProblemSolution(
        problem_id,
        f"{num_valid_range_passwords} valid passwords using range rule",
        part=1,
    )
    io_handler.set_solution(solution)

    num_valid_positional_passwords = sum(
        1
        for policy, password in parse_password_policies_and_passwords(
            io_handler.input_reader, use_range_policy=False
        )
        if policy.is_valid(password)
    )
    solution = ProblemSolution(
        problem_id,
        f"{num_valid_positional_passwords} valid passwords using positional rule",
        part=2,
    )
    io_handler.set_solution(solution)
