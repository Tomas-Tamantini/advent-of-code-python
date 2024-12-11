from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .transform_stones import transform_stones


def aoc_2024_d11(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 11, "Plutonian Pebbles")
    io_handler.output_writer.write_header(problem_id)
    stones = list(map(int, io_handler.input_reader.read().split()))

    transformed = stones[:]
    for _ in range(25):
        transformed = list(transform_stones(transformed))
    num_transformed = len(transformed)
    yield ProblemSolution(
        problem_id,
        f"The number of stones after 25 transformations is {num_transformed}",
        result=num_transformed,
        part=1,
    )
