from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_scratchcards


def aoc_2023_d4(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 4, "Scratchcards")
    io_handler.output_writer.write_header(problem_id)
    cards = list(parse_scratchcards(io_handler.input_reader))

    total_num_points = sum(card.num_points() for card in cards)
    yield ProblemSolution(
        problem_id,
        f"Part 1: The total number of points is {total_num_points}",
        result=total_num_points,
        part=1,
    )
