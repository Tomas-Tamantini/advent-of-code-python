from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_passports
from .passport import PASSPORT_RULES, passport_is_valid


def aoc_2020_d4(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 4, "Passport Processing")
    io_handler.output_writer.write_header(problem_id)
    passports = list(parse_passports(io_handler.input_reader))
    required_fields = set(PASSPORT_RULES.keys())
    passports_with_all_fields = [
        passport for passport in passports if required_fields.issubset(passport.keys())
    ]
    solution = ProblemSolution(
        problem_id,
        f"{len(passports_with_all_fields)} passports with all fields",
        part=1,
    )
    io_handler.set_solution(solution)

    num_valid_passports = sum(
        passport_is_valid(passport, PASSPORT_RULES) for passport in passports
    )
    solution = ProblemSolution(
        problem_id, f"{num_valid_passports} valid passports", part=2
    )
    io_handler.set_solution(solution)
