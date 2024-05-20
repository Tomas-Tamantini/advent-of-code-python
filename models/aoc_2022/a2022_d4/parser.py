from typing import Iterator
from models.common.io import InputReader
from models.common.number_theory import Interval


def _parse_interval(interval_str: str) -> Interval:
    min_inclusive, max_inclusive = map(int, interval_str.split("-"))
    return Interval(min_inclusive, max_inclusive)


def parse_interval_pairs(
    input_reader: InputReader,
) -> Iterator[tuple[Interval, Interval]]:
    for line in input_reader.read_stripped_lines():
        intervals = map(_parse_interval, line.split(","))
        yield tuple(intervals)
