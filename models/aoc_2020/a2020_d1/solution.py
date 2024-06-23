from models.common.io import IOHandler, Problem, ProblemSolution
from .subset_sum import subsets_that_sum_to


def aoc_2020_d1(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 1, "Report Repair")
    io_handler.output_writer.write_header(problem_id)
    entries = [int(line) for line in io_handler.input_reader.readlines()]
    target_sum = 2020
    a, b = next(subsets_that_sum_to(target_sum, subset_size=2, entries=entries))
    solution = ProblemSolution(
        problem_id, f"The two entries multiply to {a * b}", part=1
    )
    io_handler.output_writer.write_solution(solution)
    a, b, c = next(subsets_that_sum_to(target_sum, subset_size=3, entries=entries))
    solution = ProblemSolution(
        problem_id, f"The three entries multiply to {a * b * c}", part=2
    )
    io_handler.output_writer.write_solution(solution)
