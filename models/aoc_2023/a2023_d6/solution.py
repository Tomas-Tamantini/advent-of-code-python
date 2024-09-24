from typing import Iterator, Iterable
from math import prod
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_boat_races
from .boat_race import number_of_ways_to_beat_boat_race_record, BoatRace


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
        f"The product of the number of ways to beat the record is {product_with_whitespaces}",
        result=product_with_whitespaces,
        part=1,
    )

    races_without_whitespaces = parse_boat_races(
        io_handler.input_reader, consider_white_spaces=False
    )
    product_without_whitespaces = _product(races_without_whitespaces)
    yield ProblemSolution(
        problem_id,
        f"The number of ways to beat the record in the longer race is {product_without_whitespaces}",
        result=product_without_whitespaces,
        part=2,
    )
