from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .digit_finder import find_digits


def _calibration_values(sequence: str, include_spelled_out: bool = False) -> int:
    digits = list(find_digits(sequence, include_spelled_out))
    return digits[0].value * 10 + digits[-1].value


def aoc_2023_d1(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 1, "Trebuchet?!")
    io_handler.output_writer.write_header(problem_id)
    sequences = list(io_handler.input_reader.read_stripped_lines())

    result = sum(_calibration_values(sequence) for sequence in sequences)
    yield ProblemSolution(
        problem_id, f"The sum of calibation values is {result}", result, part=1
    )

    result = sum(
        _calibration_values(sequence, include_spelled_out=True)
        for sequence in sequences
    )
    yield ProblemSolution(
        problem_id,
        f"The sum of calibation values including spelled out digits is {result}",
        result,
        part=2,
    )
