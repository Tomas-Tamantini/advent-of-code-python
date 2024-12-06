from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_program_tree


def aoc_2017_d7(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 7, "Recursive Circus")
    io_handler.output_writer.write_header(problem_id)
    root = parse_program_tree(io_handler.input_reader)
    yield ProblemSolution(
        problem_id, f"Root node: {root.name}", part=1, result=root.name
    )

    imbalance = root.weight_imbalance()
    yield ProblemSolution(
        problem_id,
        f"Weight to fix imbalance: {imbalance.expected_weight}",
        part=2,
        result=imbalance.expected_weight,
    )
