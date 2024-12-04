from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from .logic import find_words, find_x_shaped_words


def aoc_2024_d4(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 4, "Ceres Search")
    io_handler.output_writer.write_header(problem_id)
    puzzle = CharacterGrid(io_handler.input_reader.read())
    num_words = len(list(find_words("XMAS", puzzle)))
    yield ProblemSolution(
        problem_id,
        f"The number of times the word 'XMAS' appears is {num_words}",
        result=num_words,
        part=1,
    )

    num_x_words = len(list(find_x_shaped_words("MAS", puzzle)))
    yield ProblemSolution(
        problem_id,
        f"The number of times the x-shaped word 'MAS' appears is {num_x_words}",
        result=num_x_words,
        part=2,
    )
