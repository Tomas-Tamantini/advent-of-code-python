from models.common.io import InputFromString
from models.common.number_theory import Interval

from ..parser import (
    parse_maps,
    parse_seeds_as_intervals,
    parse_seeds_as_standalone_intervals,
)

file_content = """seeds: 79 14 55 13

                  seed-to-soil map:
                  50 98 2
                  52 50 48

                  soil-to-fertilizer map:
                  0 15 37
                  37 52 2
                  39 0 15"""


def test_parse_maps_parses_all_maps():
    input_reader = InputFromString(file_content)
    maps = list(parse_maps(input_reader))
    assert len(maps) == 2
    assert set(maps[0].map_interval(Interval(0, 100))) == {
        Interval(0, 49),
        Interval(52, 99),
        Interval(50, 51),
        Interval(100, 100),
    }


def test_parse_seeds_as_standalone_intervals_returns_length_one_intervals():
    input_reader = InputFromString(file_content)
    seeds = list(parse_seeds_as_standalone_intervals(input_reader))
    assert seeds == [
        Interval(79, 79),
        Interval(14, 14),
        Interval(55, 55),
        Interval(13, 13),
    ]


def test_parse_seeds_as_intervals_uses_given_interval_lenghts():
    input_reader = InputFromString(file_content)
    seeds = list(parse_seeds_as_intervals(input_reader))
    assert seeds == [Interval(79, 92), Interval(55, 67)]
