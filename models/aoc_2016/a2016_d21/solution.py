from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_string_scrambler


def aoc_2016_d21(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2016, 21, "Scrambled Letters and Hash")
    io_handler.output_writer.write_header(problem_id)
    scrambler = parse_string_scrambler(io_handler.input_reader)
    password = scrambler.scramble("abcdefgh")
    yield ProblemSolution(
        problem_id, f"Password after scrambling: {password}", part=1, result=password
    )

    password = scrambler.unscramble("fbgdceah")
    yield ProblemSolution(
        problem_id, f"Password before scrambling: {password}", part=2, result=password
    )
