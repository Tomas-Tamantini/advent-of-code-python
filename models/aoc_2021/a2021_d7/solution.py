from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .optimal_fuel_consumption import (
    optimal_linear_fuel_consumption,
    optimal_triangular_fuel_consumption,
)


def aoc_2021_d7(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2021, 7, "The Treachery of Whales")
    io_handler.output_writer.write_header(problem_id)
    positions = list(map(int, io_handler.input_reader.read().split(",")))

    optimal_linear = optimal_linear_fuel_consumption(positions)
    yield ProblemSolution(
        problem_id,
        f"The total fuel required with linear consumption is {optimal_linear}",
        part=1,
        result=optimal_linear,
    )

    optimal_triangular = optimal_triangular_fuel_consumption(positions)
    yield ProblemSolution(
        problem_id,
        f"The total fuel required with triangular consumption is {optimal_triangular}",
        part=2,
        result=optimal_triangular,
    )
