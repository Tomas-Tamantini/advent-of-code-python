from typing import Protocol, Iterator, Optional
from dataclasses import dataclass
from models.common.number_theory import Interval


class IntervalMapper(Protocol):
    def map_interval(self, interval: Interval) -> Iterator[Interval]: ...


@dataclass(frozen=True)
class IntervalOffset:
    interval: Interval
    offset_value: int

    def shifted_interval(self, interval: Interval) -> Optional[Interval]:
        intersection = interval.intersection(self.interval)
        if intersection:
            return intersection.offset(self.offset_value)


class PiecewiseIntervalMapper:
    def __init__(self, *offsets: IntervalOffset) -> None:
        self._offsets = offsets

    def map_interval(self, interval: Interval) -> Iterator[Interval]:
        remaining_intervals = [interval]
        shifted_intervals = []

        for offset in self._offsets:
            new_remaining = []
            for remaining_interval in remaining_intervals:
                new_remaining.extend(remaining_interval - offset.interval)
                shifted = offset.shifted_interval(remaining_interval)
                if shifted is not None:
                    shifted_intervals.append(shifted)
            remaining_intervals = new_remaining

        yield from shifted_intervals
        yield from remaining_intervals


class CompositeIntervalMapper:
    def __init__(self, *submappers: IntervalMapper) -> None:
        self._submappers = submappers

    def map_interval(self, interval: Interval) -> Iterator[Interval]:
        input_intervals = [interval]
        output_intervals = []
        for submapper in self._submappers:
            for input_interval in input_intervals:
                output_intervals.extend(submapper.map_interval(input_interval))
            input_intervals = output_intervals
            output_intervals = []
        yield from input_intervals
