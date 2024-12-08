from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import num_arrangements_nonogram_row
from .parser import parse_nonogram_rows


def aoc_2023_d12(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 12, "Hot Springs")
    io_handler.output_writer.write_header(problem_id)

    arrangements_no_repetition = sum(
        num_arrangements_nonogram_row(row)
        for row in parse_nonogram_rows(io_handler.input_reader, number_of_repetitions=1)
    )
    yield ProblemSolution(
        problem_id,
        (
            "The number of arrangements ignoring "
            f"repetitions is {arrangements_no_repetition}"
        ),
        result=arrangements_no_repetition,
        part=1,
    )

    arrangements_with_repetition = sum(
        num_arrangements_nonogram_row(row)
        for row in parse_nonogram_rows(io_handler.input_reader, number_of_repetitions=5)
    )
    yield ProblemSolution(
        problem_id,
        (
            "The number of arrangements with "
            f"repetitions is {arrangements_with_repetition}"
        ),
        result=arrangements_with_repetition,
        part=2,
    )
