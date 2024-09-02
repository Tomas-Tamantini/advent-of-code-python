from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_scratchcards
from .scratchcard import number_of_cards_after_prizes


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

    total_num_cards = number_of_cards_after_prizes(cards)
    yield ProblemSolution(
        problem_id,
        f"Part 2: They end up with {total_num_cards} cards",
        result=total_num_cards,
        part=2,
    )
