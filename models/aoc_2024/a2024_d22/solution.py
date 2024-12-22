from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .pseudo_random import maximize_winnings, pseudo_random_sequence


def aoc_2024_d22(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 22, "Monkey Market")
    io_handler.output_writer.write_header(problem_id)
    secret_numbers = [int(num) for num in io_handler.input_reader.read_stripped_lines()]
    num_iterations = 2000

    total = 0
    for i, n in enumerate(secret_numbers):
        io_handler.progress_bar.update(i, len(secret_numbers))
        sequence = tuple(pseudo_random_sequence(n, num_iterations))
        total += sequence[-1]

    yield ProblemSolution(
        problem_id, f"The sum of generated numbers is {total}", result=total, part=1
    )

    max_winnings = maximize_winnings(
        secret_numbers, num_iterations, io_handler.progress_bar
    )
    yield ProblemSolution(
        problem_id,
        f"The maximum winnings are {max_winnings}",
        result=max_winnings,
        part=2,
    )
