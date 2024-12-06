from typing import Iterator

from models.common.io import CharacterGrid, IOHandler, Problem, ProblemSolution

from .galaxies import Galaxies


def aoc_2023_d11(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 11, "Cosmic Expansion")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    positions = set(grid.positions_with_value("#"))
    galaxies = Galaxies(positions)

    distance_exp_2 = sum(
        galaxies.distance_between(*pair, expansion_rate=2)
        for pair in galaxies.pairwise_galaxies()
    )

    yield ProblemSolution(
        problem_id,
        f"Distance between pairs of galaxies with expansion rate 2 is {distance_exp_2}",
        result=distance_exp_2,
        part=1,
    )

    distance_exp_1m = sum(
        galaxies.distance_between(*pair, expansion_rate=1_000_000)
        for pair in galaxies.pairwise_galaxies()
    )

    yield ProblemSolution(
        problem_id,
        f"Distance between pairs of galaxies with expansion rate 1,000,000 is {distance_exp_1m}",
        result=distance_exp_1m,
        part=2,
    )
