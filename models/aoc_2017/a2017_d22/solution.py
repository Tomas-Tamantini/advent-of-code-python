from typing import Iterator

from models.common.io import CharacterGrid, IOHandler, Problem, ProblemSolution
from models.common.vectors import CardinalDirection

from .grid_cluster import GridCluster


def aoc_2017_d22(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 22, "Sporifica Virus")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    infected_positions = set(grid.positions_with_value("#"))
    cluster = GridCluster(
        carrier_position=grid.center,
        carrier_direction=CardinalDirection.SOUTH,
        currently_infected=infected_positions,
    )
    num_infections_two_state = cluster.total_number_of_infections_caused(10_000)
    yield ProblemSolution(
        problem_id,
        (
            "The number of infections caused with two-state carrier is "
            f"{num_infections_two_state}"
        ),
        part=1,
        result=num_infections_two_state,
    )

    num_infections_four_state = cluster.total_number_of_infections_caused(
        10_000_000, use_four_states=True, progress_bar=io_handler.progress_bar
    )
    yield ProblemSolution(
        problem_id,
        (
            "The number of infections caused with four-state carrier is "
            f"{num_infections_four_state}"
        ),
        part=2,
        result=num_infections_four_state,
    )
