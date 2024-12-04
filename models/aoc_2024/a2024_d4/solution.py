from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from .logic import find_words


def aoc_2024_d4(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2024, 4, "Ceres Search")
    io_handler.output_writer.write_header(problem_id)
    puzzle = CharacterGrid(io_handler.input_reader.read())
    words = list(find_words("XMAS", puzzle))
    num_words = len(words)
    yield ProblemSolution(
        problem_id,
        f"The word 'XMAS' appears {num_words} times in the puzzle",
        result=num_words,
        part=1,
    )
