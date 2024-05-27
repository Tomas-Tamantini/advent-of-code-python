from models.common.io import InputReader, CharacterGrid
from models.common.vectors import Vector2D
from .underwater_cave import UnderwaterCaveMaze


def aoc_2021_d15(input_reader: InputReader, **_) -> None:
    print("--- AOC 2021 - Day 15: Chiton ---")
    grid = CharacterGrid(input_reader.read())
    cave_maze = UnderwaterCaveMaze(
        risk_levels={pos: int(char) for pos, char in grid.tiles.items()},
        extension_factor=1,
    )
    start = Vector2D(0, 0)
    end = Vector2D(grid.width - 1, grid.height - 1)
    risk_level = cave_maze.risk_of_optimal_path(start, end)
    print(f"Part 1: The risk level of the optimal path is {risk_level}")

    extension_factor = 5
    cave_maze = UnderwaterCaveMaze(
        risk_levels={pos: int(char) for pos, char in grid.tiles.items()},
        extension_factor=extension_factor,
    )
    end = Vector2D(
        grid.width * extension_factor - 1, grid.height * extension_factor - 1
    )
    risk_level = cave_maze.risk_of_optimal_path(start, end)
    print(
        f"Part 2: The risk level of the optimal path in the extended cave is {risk_level}"
    )
