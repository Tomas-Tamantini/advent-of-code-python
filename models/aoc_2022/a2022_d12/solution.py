from typing import Iterator

from models.common.io import CharacterGrid, IOHandler, Problem, ProblemSolution

from .hill_maze import HillMaze


def aoc_2022_d12(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2022, 12, "Hill Climbing Algorithm")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    maze = HillMaze(grid)
    min_num_steps = maze.min_num_steps_to_destination("S", "E")
    yield ProblemSolution(
        problem_id,
        f"Minimum number of steps to reach destination is {min_num_steps}",
        part=1,
        result=min_num_steps,
    )

    min_num_steps = min(min_num_steps, maze.min_num_steps_to_destination("a", "E"))
    yield ProblemSolution(
        problem_id,
        (
            "Minimum number of steps to reach destination "
            f"from any cell of height 'a' is {min_num_steps}"
        ),
        part=2,
        result=min_num_steps,
    )
