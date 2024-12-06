from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import minimum_cut_partition
from .parser import parse_wiring_diagram


def aoc_2023_d25(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 25, "Snowverload")
    io_handler.output_writer.write_header(problem_id)
    graph = parse_wiring_diagram(io_handler.input_reader)
    left, right = minimum_cut_partition(
        graph, minimum_cut_lower_bound=3, progress_bar=io_handler.progress_bar
    )
    product = len(left) * len(right)
    yield ProblemSolution(
        problem_id,
        f"The product of the sizes of each minimum cut partition is {product}",
        result=product,
    )
