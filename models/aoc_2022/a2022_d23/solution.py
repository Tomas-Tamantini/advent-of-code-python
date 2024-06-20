from models.common.io import InputReader, CharacterGrid
from models.common.vectors import CardinalDirection, BoundingBox
from .logic import AntisocialElves, direction_priority


def aoc_2022_d23(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 23: Unstable Diffusion ---")
    grid = CharacterGrid(input_reader.read())
    positions = set(grid.positions_with_value("#"))
    elves = AntisocialElves(positions)
    priority_first_round = [
        CardinalDirection.NORTH,
        CardinalDirection.SOUTH,
        CardinalDirection.WEST,
        CardinalDirection.EAST,
    ]
    for round in range(10):
        priority = direction_priority(priority_first_round, round)
        elves.move(priority)

    bounding_box = BoundingBox.from_points(elves.positions)
    num_elves = len(elves.positions)
    empty_spaces = (bounding_box.width + 1) * (bounding_box.height + 1) - num_elves
    print(f"Part 1: After 10 moves, the number of ground tiles is {empty_spaces}.")
