from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .navigation_tree import parse_list_into_navigation_tree


def aoc_2018_d8(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2018, 8, "Memory Maneuver")
    io_handler.output_writer.write_header(problem_id)
    numbers = list(map(int, io_handler.input_reader.read().split()))
    root = parse_list_into_navigation_tree(numbers)
    result = root.sum_of_metadata()
    yield ProblemSolution(problem_id, f"Sum of metadata: {result}", result, part=1)
    result = root.navigation_value()
    yield ProblemSolution(problem_id, f"Value of root node: {result}", result, part=2)
