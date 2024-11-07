from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from .logic import max_length_non_repeating_path
from .parser import parse_forest_map


def aoc_2023_d23(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 23, "A Long Walk")
    io_handler.output_writer.write_header(problem_id)

    grid = CharacterGrid(io_handler.input_reader.read())
    tiles = list(grid.positions_with_value("."))
    start = min(tiles, key=lambda p: p.y)
    end = max(tiles, key=lambda p: p.y)

    slope_maze = parse_forest_map(grid, consider_slopes=True)
    slope_maze.reduce(irreducible_nodes={start, end})
    slope_length = max_length_non_repeating_path(slope_maze, start, end)
    yield ProblemSolution(
        problem_id,
        f"The max. number of steps considering slopes is {slope_length}",
        result=slope_length,
        part=1,
    )

    flat_maze = parse_forest_map(grid, consider_slopes=False)
    flat_maze.reduce(irreducible_nodes={start, end})
    io_handler.output_writer.give_time_estimation("2min", part=2)
    flat_length = max_length_non_repeating_path(flat_maze, start, end)
    yield ProblemSolution(
        problem_id,
        f"The max. number of steps ignoring slopes is {flat_length}",
        result=flat_length,
        part=2,
    )
