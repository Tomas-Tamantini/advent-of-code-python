from models.common.io import IOHandler
from models.common.vectors import Vector2D
from .parser import parse_obstacles
from .falling_sand import FallingSand


def aoc_2022_d14(io_handler: IOHandler) -> None:
    print("--- AOC 2022 - Day 14: Regolith Reservoir ---")
    obstacles = set(parse_obstacles(io_handler.input_reader))
    sand_pour_position = Vector2D(500, 0)
    falling_sand = FallingSand(sand_pour_position, obstacles)
    falling_sand.pour_until_steady_state()
    num_resting = len(falling_sand.resting_sand_positions)
    print(f"Part 1: Number of resting sand grains is {num_resting}")
    floor_y_coord = falling_sand.max_obstacle_depth + 2
    falling_sand = FallingSand(sand_pour_position, obstacles, floor_y_coord)
    falling_sand.pour_until_source_blocked()
    num_resting = len(falling_sand.resting_sand_positions)
    print(f"Part 2: Number of resting sand grains considering floor is {num_resting}")
