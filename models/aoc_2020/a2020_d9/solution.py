from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .xmas_encoding import XMasEncoding


def aoc_2020_d9(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2020, 9, "Encoding Error")
    io_handler.output_writer.write_header(problem_id)
    numbers = [int(line) for line in io_handler.input_reader.readlines()]
    encoding = XMasEncoding(preamble_length=25)
    invalid_number = next(encoding.invalid_numbers(numbers))
    yield ProblemSolution(
        problem_id,
        f"The first invalid number is {invalid_number}",
        part=1,
        result=invalid_number,
    )

    contiguous_numbers = next(
        encoding.contiguous_numbers_which_sum_to_target(numbers, target=invalid_number)
    )
    min_num, max_num = min(contiguous_numbers), max(contiguous_numbers)
    result = min_num + max_num
    yield ProblemSolution(
        problem_id,
        f"The sum of min and max contiguous numbers is {result}",
        result,
        part=2,
    )
