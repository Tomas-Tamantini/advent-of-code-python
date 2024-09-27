from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from .logic import PipeMaze
from models.common.vectors import Polygon


def aoc_2023_d10(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 10, "Pipe Maze")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    maze = PipeMaze(grid)
    loop = tuple(maze.loop_positions())

    furthest = len(loop) // 2
    yield ProblemSolution(
        problem_id, f"The distance to furthest point is {furthest}", furthest, part=1
    )

    num_inside = Polygon(loop).num_grid_points_inside()
    yield ProblemSolution(
        problem_id,
        f"The number of points inside the loop is {num_inside}",
        num_inside,
        part=2,
    )
