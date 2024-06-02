from models.common.io import InputReader
from .parser import parse_portal_maze, parse_recursive_donut_maze


def aoc_2019_d20(input_reader: InputReader, **_) -> None:
    print("--- AOC 2019 - Day 20: Donut Maze ---")
    portal_maze = parse_portal_maze(input_reader)
    num_steps = portal_maze.num_steps_to_solve()
    print(
        f"Part 1: Fewest number of steps to reach the exit in Donut Maze is {num_steps}"
    )
    recursive_maze = parse_recursive_donut_maze(input_reader)
    num_steps = recursive_maze.num_steps_to_solve()
    print(
        f"Part 2: Fewest number of steps to reach the exit in Recursive Donut Maze is {num_steps}"
    )
