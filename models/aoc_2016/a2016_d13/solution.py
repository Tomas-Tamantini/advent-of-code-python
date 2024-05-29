from models.common.io import InputReader
from models.common.vectors import Vector2D
from .cubicle_maze import CubicleMaze, is_wall


def aoc_2016_d13(input_reader: InputReader, **_) -> None:
    print("--- AOC 2016 - Day 13: A Maze of Twisty Little Cubicles ---")
    polynomial_offset = int(input_reader.read().strip())
    maze = CubicleMaze(
        is_wall=lambda position: is_wall(position, polynomial_offset),
        destination=Vector2D(31, 39),
    )
    origin = Vector2D(1, 1)
    num_steps = maze.length_shortest_path(initial_position=origin)
    print(f"Part 1: Fewest number of steps to reach destination: {num_steps}")
    max_steps = 50
    num_reachable = maze.number_of_reachable_cubicles(origin, max_steps)
    print(
        f"Part 2: Number of cubicles reachable in at most {max_steps} steps: {num_reachable}"
    )