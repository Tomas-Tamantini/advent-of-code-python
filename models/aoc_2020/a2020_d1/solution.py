from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .subset_sum import subsets_that_sum_to


def aoc_2020_d1(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2020, 1, "Report Repair")
    io_handler.output_writer.write_header(problem_id)
    entries = [int(line) for line in io_handler.input_reader.readlines()]
    target_sum = 2020
    a, b = next(subsets_that_sum_to(target_sum, subset_size=2, entries=entries))
    result = a * b
    yield ProblemSolution(
        problem_id, f"The two entries multiply to {result}", result, part=1
    )

    a, b, c = next(subsets_that_sum_to(target_sum, subset_size=3, entries=entries))
    result = a * b * c
    yield ProblemSolution(
        problem_id, f"The three entries multiply to {result}", result, part=2
    )
