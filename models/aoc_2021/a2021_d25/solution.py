from models.common.io import InputReader, CharacterGrid
from .sea_cucumber import SeaCucumbers, SeaCucumbersHerds


def aoc_2021_d25(input_reader: InputReader, **_) -> None:
    print("--- AOC 2021 - Day 25: Sea Cucumber ---")
    grid = CharacterGrid(input_reader.read())
    sea_cucumbers = SeaCucumbers(width=grid.width, height=grid.height)
    herds = SeaCucumbersHerds(
        east_facing=set(grid.positions_with_value(">")),
        south_facing=set(grid.positions_with_value("v")),
    )
    num_steps = sea_cucumbers.num_steps_until_halt(herds)
    print(f"The number of steps until the herds stop moving is {num_steps}")
