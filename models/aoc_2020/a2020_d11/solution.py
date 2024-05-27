from models.common.io import InputReader, CharacterGrid
from .ferry_seats import FerrySeats, FerrySeat


def aoc_2020_d11(input_reader: InputReader, **_) -> None:
    print("--- AOC 2020 - Day 11: Seating System ---")
    grid = CharacterGrid(input_reader.read())

    ferry_adjacent_only = FerrySeats(
        width=grid.width,
        height=grid.height,
        initial_configuration=grid.tiles,
        occupied_neighbors_tolerance=3,
        consider_only_adjacent_neighbors=True,
    )
    final_state = ferry_adjacent_only.steady_state()
    num_occupied = list(final_state.values()).count(FerrySeat.OCCUPIED)
    print(f"Part 1: Occupied seats considering only adjacent neighbors: {num_occupied}")

    ferry_first_chair = FerrySeats(
        width=grid.width,
        height=grid.height,
        initial_configuration=grid.tiles,
        occupied_neighbors_tolerance=4,
        consider_only_adjacent_neighbors=False,
    )
    final_state = ferry_first_chair.steady_state()
    num_occupied = list(final_state.values()).count(FerrySeat.OCCUPIED)
    print(
        f"Part 2: Occupied seats considering first chair in line of sight: {num_occupied}"
    )
