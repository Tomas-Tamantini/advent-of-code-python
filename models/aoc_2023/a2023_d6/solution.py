from math import prod
from typing import Iterable, Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .boat_race import BoatRace, number_of_ways_to_beat_boat_race_record
from .parser import parse_boat_races


def _product(races: Iterable[BoatRace]) -> int:
    return prod(number_of_ways_to_beat_boat_race_record(race) for race in races)


def aoc_2023_d6(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 6, "Wait For It")
    io_handler.output_writer.write_header(problem_id)
    races_with_whitespaces = parse_boat_races(
        io_handler.input_reader, consider_white_spaces=True
    )
    product_with_whitespaces = _product(races_with_whitespaces)
    yield ProblemSolution(
        problem_id,
        (
            "The product of the number of ways to beat the record is "
            f"{product_with_whitespaces}"
        ),
        result=product_with_whitespaces,
        part=1,
    )

    races_without_whitespaces = parse_boat_races(
        io_handler.input_reader, consider_white_spaces=False
    )
    product_without_whitespaces = _product(races_without_whitespaces)
    yield ProblemSolution(
        problem_id,
        (
            "The number of ways to beat the record in the longer race is "
            f"{product_without_whitespaces}"
        ),
        result=product_without_whitespaces,
        part=2,
    )
