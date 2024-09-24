from typing import Iterator, Iterable
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_camel_bids, CamelBid


def _winnings(bids: Iterable[CamelBid]) -> int:
    winnings = 0
    for i, bid in enumerate(sorted(bids)):
        winnings += (i + 1) * bid.bid_value
    return winnings


def aoc_2023_d7(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 7, "Camel Cards")
    io_handler.output_writer.write_header(problem_id)
    winnings_without_joker = _winnings(
        parse_camel_bids(io_handler.input_reader, include_joker=False)
    )
    yield ProblemSolution(
        problem_id,
        f"The total winnings without the jokers are {winnings_without_joker}",
        result=winnings_without_joker,
        part=1,
    )

    winnings_with_joker = _winnings(
        parse_camel_bids(io_handler.input_reader, include_joker=True)
    )
    yield ProblemSolution(
        problem_id,
        f"The total winnings with the jokers are {winnings_with_joker}",
        result=winnings_with_joker,
        part=2,
    )
