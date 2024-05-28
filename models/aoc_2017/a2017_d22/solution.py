from models.common.io import InputReader, CharacterGrid, ProgressBarConsole
from models.common.vectors import CardinalDirection
from .grid_cluster import GridCluster


def aoc_2017_d22(
    input_reader: InputReader, progress_bar: ProgressBarConsole, **_
) -> None:
    print("--- AOC 2017 - Day 22: Sporifica Virus ---")
    grid = CharacterGrid(input_reader.read())
    infected_positions = set(grid.positions_with_value("#"))
    cluster = GridCluster(
        carrier_position=grid.center,
        carrier_direction=CardinalDirection.SOUTH,
        currently_infected=infected_positions,
    )
    num_infections_two_state = cluster.total_number_of_infections_caused(10_000)
    print(
        f"Part 1: Number of infections caused with two-state carrier: {num_infections_two_state}"
    )
    num_infections_four_state = cluster.total_number_of_infections_caused(
        10_000_000, use_four_states=True, progress_bar=progress_bar
    )
    print(
        f"Part 2: Number of infections caused with four-state carrier: {num_infections_four_state}"
    )
