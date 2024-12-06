from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .aunt_sue import MatchType
from .parser import parse_aunt_sue_collection


def aoc_2015_d16(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2015, 16, "Aunt Sue")
    io_handler.output_writer.write_header(problem_id)
    measured_attributes = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }
    measured_attributes_exact = {
        attribute: (value, MatchType.EXACT)
        for attribute, value in measured_attributes.items()
    }

    def match_type(attribute: str) -> MatchType:
        if attribute in {"cats", "trees"}:
            return MatchType.GREATER_THAN
        elif attribute in {"pomeranians", "goldfish"}:
            return MatchType.LESS_THAN
        else:
            return MatchType.EXACT

    measure_attributes_retroencabulator = {
        attribute: (value, match_type(attribute))
        for attribute, value in measured_attributes.items()
    }
    aunts = parse_aunt_sue_collection(io_handler.input_reader)
    for aunt in aunts:
        if aunt.matches(measured_attributes_exact):
            yield ProblemSolution(
                problem_id,
                f"Aunt Sue {aunt.id} matches exact data",
                part=1,
                result=aunt.id,
            )

        if aunt.matches(measure_attributes_retroencabulator):
            yield ProblemSolution(
                problem_id,
                f"Aunt Sue {aunt.id} matches range data",
                part=2,
                result=aunt.id,
            )
