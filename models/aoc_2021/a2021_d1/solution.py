from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution


def num_increases(lst: list[int]) -> int:
    return sum(lst[i] > lst[i - 1] for i in range(1, len(lst)))


def window_sum(lst: list[int], window_size: int) -> list[int]:
    return [sum(lst[i : i + window_size]) for i in range(len(lst) - window_size + 1)]


def aoc_2021_d1(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2021, 1, "Sonar Sweep")
    io_handler.output_writer.write_header(problem_id)
    measurements = [int(line) for line in io_handler.input_reader.readlines()]

    yield ProblemSolution(
        problem_id,
        f"The number of measurement increases is {num_increases(measurements)}",
        part=1,
    )

    sums = window_sum(measurements, window_size=3)
    yield ProblemSolution(
        problem_id,
        f"The number of increases in partial sums is {num_increases(sums)}",
        part=2,
    )
