from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from .logic import Gardener, BoundedGarden


def aoc_2023_d21(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 21, "Step Counter")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    rock_positions = set(grid.positions_with_value("#"))
    initial_position = next(grid.positions_with_value("S"))
    gardener = Gardener(initial_position)
    bounded_garden = BoundedGarden(grid.width, grid.height, rock_positions)
    series_generator = gardener.num_reachable_positions(bounded_garden)
    series = [next(series_generator) for _ in range(65)]

    num_plots = series[-1]
    yield ProblemSolution(
        problem_id,
        f"The number of garden plots the gardener can reach in bounded garden is {num_plots}",
        result=num_plots,
        part=1,
    )
