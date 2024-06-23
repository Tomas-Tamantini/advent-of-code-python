from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from .hill_maze import HillMaze


def aoc_2022_d12(io_handler: IOHandler) -> None:
    problem_id = Problem(2022, 12, "Hill Climbing Algorithm")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    maze = HillMaze(grid)
    min_num_steps = maze.min_num_steps_to_destination("S", "E")
    solution = ProblemSolution(
        problem_id,
        f"Minimum number of steps to reach destination is {min_num_steps}",
        part=1,
    )
    io_handler.output_writer.write_solution(solution)
    min_num_steps = min(min_num_steps, maze.min_num_steps_to_destination("a", "E"))
    solution = ProblemSolution(
        problem_id,
        f"Minimum number of steps to reach destination from any cell of height 'a' is {min_num_steps}",
        part=2,
    )
    io_handler.output_writer.write_solution(solution)
