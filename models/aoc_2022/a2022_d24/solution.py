from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_blizzard_valley
from .logic import BlizzardMazeSolver


def aoc_2022_d24(io_handler: IOHandler) -> None:
    problem_id = Problem(2022, 24, "Blizzard Basin")
    io_handler.output_writer.write_header(problem_id)
    valley = parse_blizzard_valley(io_handler.input_reader)
    solver = BlizzardMazeSolver(valley)
    io_handler.output_writer.give_time_estimation("20s", part=1)
    min_steps = solver.min_steps_to_exit()
    solution = ProblemSolution(
        problem_id, f"The minimum number of steps to exit valley is {min_steps}", part=1
    )
    io_handler.set_solution(solution)
    io_handler.output_writer.give_time_estimation("1min", part=2)
    min_steps = solver.min_steps_to_exit(num_returns_to_start=1)
    solution = ProblemSolution(
        problem_id,
        f"The minimum number of steps to exit valley twice is {min_steps}",
        part=2,
    )
    io_handler.set_solution(solution)
