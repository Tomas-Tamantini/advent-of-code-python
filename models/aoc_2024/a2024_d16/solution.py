from typing import Iterator

from models.common.io import CharacterGrid, IOHandler, Problem, ProblemSolution
from models.common.vectors import CardinalDirection

from .reindeer_maze import ReindeerMaze


def _parse_maze(grid: CharacterGrid) -> ReindeerMaze:
    start_tile = next(grid.positions_with_value("S"))
    start_direction = CardinalDirection.EAST
    end_tile = next(grid.positions_with_value("E"))
    maze_tiles = set(grid.positions_with_value(".")) | {start_tile, end_tile}
    return ReindeerMaze(start_tile, start_direction, end_tile, maze_tiles)


def aoc_2024_d16(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 16, "Reindeer Maze")
    io_handler.output_writer.write_header(problem_id)
    maze = _parse_maze(CharacterGrid(io_handler.input_reader.read()))

    min_score = maze.minimal_score()
    yield ProblemSolution(
        problem_id,
        f"The minimal score for the reindeer to complete the maze is {min_score}",
        result=min_score,
        part=1,
    )
    io_handler.output_writer.give_time_estimation("10s", part=2)
    num_tiles = len(set(maze.tiles_on_optimal_paths()))
    yield ProblemSolution(
        problem_id,
        f"The number of tiles on the optimal paths is {num_tiles}",
        result=num_tiles,
        part=2,
    )
