from models.common.io import IOHandler, Problem, ProblemSolution
from .memory_game import memory_game_numbers


def aoc_2020_d15(io_handler: IOHandler) -> None:
    problem_id = Problem(2020, 15, "Rambunctious Recitation")
    io_handler.output_writer.write_header(problem_id)
    starting_numbers = [
        int(number) for number in io_handler.input_reader.read().split(",")
    ]
    generator = memory_game_numbers(starting_numbers)
    numbers = [next(generator) for _ in range(2020)]
    solution = ProblemSolution(
        problem_id, f"The 2020th number spoken is {numbers[-1]}", part=1
    )
    io_handler.output_writer.write_solution(solution)
    generator = memory_game_numbers(starting_numbers)
    number = -1
    num_terms = 30_000_000
    for i in range(num_terms):
        io_handler.progress_bar.update(i, num_terms)
        number = next(generator)
    solution = ProblemSolution(
        problem_id, f"The {num_terms}th number spoken is {number}", part=2
    )
    io_handler.output_writer.write_solution(solution)
