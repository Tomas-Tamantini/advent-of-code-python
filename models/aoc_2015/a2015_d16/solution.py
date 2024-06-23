from models.common.io import IOHandler
from .parser import parse_aunt_sue_collection
from .aunt_sue import MatchType


def aoc_2015_d16(io_handler: IOHandler) -> None:
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
            print(f"Part 1: Aunt Sue {aunt.id} matches exact data")
        if aunt.matches(measure_attributes_retroencabulator):
            print(f"Part 2: Aunt Sue {aunt.id} matches range data")
