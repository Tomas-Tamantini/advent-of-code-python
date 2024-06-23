from models.common.io import IOHandler, CharacterGrid
from .hill_maze import HillMaze


def aoc_2022_d12(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2022, 12, "Hill Climbing Algorithm")
    grid = CharacterGrid(io_handler.input_reader.read())
    maze = HillMaze(grid)
    min_num_steps = maze.min_num_steps_to_destination("S", "E")
    print(f"Part 1: Minimum number of steps to reach destination is {min_num_steps}")
    min_num_steps = min(min_num_steps, maze.min_num_steps_to_destination("a", "E"))
    print(
        f"Part 2: Minimum number of steps to reach destination from any cell of height 'a' is {min_num_steps}"
    )
