from models.common.io import IOHandler, CharacterGrid
from models.common.vectors import CardinalDirection, BoundingBox
from .logic import AntisocialElves, direction_priority


def aoc_2022_d23(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2022 - Day 23: Unstable Diffusion ---")
    grid = CharacterGrid(io_handler.input_reader.read())
    positions = set(grid.positions_with_value("#"))
    priority_first_round = [
        CardinalDirection.NORTH,
        CardinalDirection.SOUTH,
        CardinalDirection.WEST,
        CardinalDirection.EAST,
    ]

    elves = AntisocialElves(positions)
    for round_index in range(10):
        priority = direction_priority(priority_first_round, round_index)
        elves.move(priority)

    bounding_box = BoundingBox.from_points(elves.positions)
    num_elves = len(elves.positions)
    empty_spaces = (bounding_box.width + 1) * (bounding_box.height + 1) - num_elves
    print(f"Part 1: After 10 moves, the number of ground tiles is {empty_spaces}")
    print("Part 2: Be patient, it takes about 20s to run", end="\r")
    round_index = 0
    elves = AntisocialElves(positions)
    while elves.num_elves_that_moved_last_round > 0:
        priority = direction_priority(priority_first_round, round_index)
        elves.move(priority)
        round_index += 1

    print(f"Part 2: Number of rounds until elves settle is {round_index}")
