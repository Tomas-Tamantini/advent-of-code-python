from typing import Iterator
from models.common.io import InputReader
from models.common.number_theory import Interval
from .interval_mapper import PiecewiseIntervalMapper, IntervalOffset


def _parse_offset(line: str) -> Interval:
    destination_start, source_start, interval_length = map(int, line.split())
    offset_value = destination_start - source_start
    source_interval = Interval(source_start, source_start + interval_length - 1)
    return IntervalOffset(interval=source_interval, offset_value=offset_value)


def _parse_seed_ranges(seeds: list[int]) -> Iterator[Interval]:
    for i in range(0, len(seeds), 2):
        range_start = seeds[i]
        range_length = seeds[i + 1]
        range_end = range_start + range_length - 1
        yield Interval(range_start, range_end)


def _seed_values(input_reader: InputReader) -> list[int]:
    for line in input_reader.read_stripped_lines():
        if "seeds:" in line:
            return list(map(int, line.split(":")[1].strip().split()))
    raise ValueError("No seeds found in input")


def parse_seeds_as_standalone_intervals(
    input_reader: InputReader,
) -> Iterator[Interval]:
    seeds = _seed_values(input_reader)
    return (Interval(int(seed), int(seed)) for seed in seeds)


def parse_seeds_as_intervals(input_reader: InputReader) -> Iterator[Interval]:
    seeds = _seed_values(input_reader)
    yield from _parse_seed_ranges(seeds)


def parse_maps(input_reader: InputReader) -> Iterator[PiecewiseIntervalMapper]:
    offsets = []
    for line in input_reader.read_stripped_lines():
        if not line or "seeds:" in line:
            continue
        elif "map:" in line:
            if offsets:
                yield PiecewiseIntervalMapper(*offsets)
                offsets = []
        else:
            offsets.append(_parse_offset(line))
    if offsets:
        yield PiecewiseIntervalMapper(*offsets)
