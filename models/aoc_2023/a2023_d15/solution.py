from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_initialization_sequence
from .logic import HashCalculator


def aoc_2023_d15(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 15, "Lens Library")
    io_handler.output_writer.write_header(problem_id)
    steps = io_handler.input_reader.read().split(",")
    calculator = HashCalculator()

    total_hash = sum(calculator.get_hash(step) for step in steps)
    yield ProblemSolution(
        problem_id, f"The sum of hash values is {total_hash}", result=total_hash, part=1
    )
