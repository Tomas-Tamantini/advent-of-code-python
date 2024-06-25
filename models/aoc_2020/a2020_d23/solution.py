from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .crab_cubs import crab_cups


def aoc_2020_d23(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2020, 23, "Crab Cups")
    io_handler.output_writer.write_header(problem_id)
    cups = [int(char) for char in io_handler.input_reader.read().strip()]
    result_lst = crab_cups(cups, num_moves=100)
    one_index = result_lst.index(1)
    result = "".join(
        str(num) for num in result_lst[one_index + 1 :] + result_lst[:one_index]
    )
    yield ProblemSolution(
        problem_id, f"Cup labels after cup 1 are {result}", result, part=1
    )

    cups += list(range(max(cups) + 1, 1_000_001))
    result_lst = crab_cups(
        cups, num_moves=10_000_000, progress_bar=io_handler.progress_bar
    )
    one_index = result_lst.index(1)
    result_lst = result_lst[one_index + 1 : one_index + 3]
    result = result_lst[0] * result_lst[1]
    yield ProblemSolution(
        problem_id, f"Product of two cups after cup 1 is {result}", result, part=2
    )
