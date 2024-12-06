from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_portal_maze, parse_recursive_donut_maze


def aoc_2019_d20(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 20, "Donut Maze")
    io_handler.output_writer.write_header(problem_id)
    portal_maze = parse_portal_maze(io_handler.input_reader)
    num_steps = portal_maze.num_steps_to_solve()
    yield ProblemSolution(
        problem_id,
        f"Fewest number of steps to reach the exit in Donut Maze is {num_steps}",
        part=1,
        result=num_steps,
    )

    recursive_maze = parse_recursive_donut_maze(io_handler.input_reader)
    num_steps = recursive_maze.num_steps_to_solve()
    yield ProblemSolution(
        problem_id,
        f"Fewest number of steps to reach the exit in Recursive Donut Maze is {num_steps}",
        part=2,
        result=num_steps,
    )
