from models.common.io import InputReader, CharacterGrid
from .hill_maze import HillMaze


def aoc_2022_d12(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 12: Hill Climbing Algorithm ---")
    grid = CharacterGrid(input_reader.read())
    maze = HillMaze(grid)
    start = next(grid.positions_with_value("S"))
    end = next(grid.positions_with_value("E"))
    min_num_steps = maze.min_num_steps_to_destination(start, end)
    print(f"Part 1: Minimum number of steps to reach destination is {min_num_steps}")
    for start in grid.positions_with_value("a"):
        try:
            new_steps = maze.min_num_steps_to_destination(start, end)
        except ValueError:
            continue
        if new_steps < min_num_steps:
            min_num_steps = new_steps
    print(
        f"Part 2: Minimum number of steps to reach destination of all starting positions: {min_num_steps}"
    )
