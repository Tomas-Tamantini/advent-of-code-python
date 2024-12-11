from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .transform_stones import num_transformed_stones


def aoc_2024_d11(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 11, "Plutonian Pebbles")
    io_handler.output_writer.write_header(problem_id)
    stones = list(map(int, io_handler.input_reader.read().split()))

    num_transformed_25 = num_transformed_stones(stones, 25)
    yield ProblemSolution(
        problem_id,
        f"The number of stones after 25 transformations is {num_transformed_25}",
        result=num_transformed_25,
        part=1,
    )

    num_transformed_75 = num_transformed_stones(stones, 75)
    yield ProblemSolution(
        problem_id,
        f"The number of stones after 75 transformations is {num_transformed_75}",
        result=num_transformed_75,
        part=2,
    )
