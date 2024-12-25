from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_keys, parse_locks


def _fits(lock: tuple[int, ...], key: tuple[int, ...]) -> bool:
    return all(a + b <= 5 for a, b in zip(lock, key))


def aoc_2024_d25(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 25, "Code Chronicle")
    io_handler.output_writer.write_header(problem_id)
    locks = list(parse_locks(io_handler.input_reader))
    keys = list(parse_keys(io_handler.input_reader))
    num_pairs = 0
    for key in keys:
        for lock in locks:
            if _fits(lock, key):
                num_pairs += 1

    yield ProblemSolution(
        problem_id,
        f"The number of pairs that fit is {num_pairs}",
        result=num_pairs,
        part=1,
    )
