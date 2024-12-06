from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_string_transformers
from .string_transform import transform_string_multiple_rounds


def aoc_2017_d16(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 16, "Permutation Promenade")
    io_handler.output_writer.write_header(problem_id)
    dance_moves = list(parse_string_transformers(io_handler.input_reader))
    dancers = "abcdefghijklmnop"
    for move in dance_moves:
        dancers = move.transform(dancers)
    yield ProblemSolution(
        problem_id, f"Final order of dancers: {dancers}", part=1, result=dancers
    )

    num_dances = 1_000_000_000
    dancers = "abcdefghijklmnop"
    dancers = transform_string_multiple_rounds(dancers, dance_moves, num_dances)
    yield ProblemSolution(
        problem_id,
        f"Final order of dancers after {num_dances} dances: {dancers}",
        part=2,
        result=dancers,
    )
