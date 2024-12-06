from typing import Iterable, Iterator

from models.common.number_theory import Interval

from .proximity_sensor import ProximitySensor


def _intersections(
    reference_interval: Interval, other_intervals: Iterable[Interval]
) -> Iterator[Interval]:
    for other in other_intervals:
        intersection = reference_interval.intersection(other)
        if intersection is not None:
            yield intersection


def _length_of_union(intervals: list[Interval]) -> int:
    if not intervals:
        return 0
    head = intervals[0]
    tail = intervals[1:]
    if not tail:
        return head.num_elements
    else:
        return (
            head.num_elements
            + _length_of_union(tail)
            - _length_of_union(list(_intersections(head, tail)))
        )


def _intervals_which_cannot_be_beacon(
    row: int, sensors: Iterable[ProximitySensor]
) -> Iterator[Interval]:
    for sensor in sensors:
        interval = sensor.interval_which_cannot_be_beacon(row)
        if interval is not None:
            yield interval


def num_positions_which_cannot_contain_beacon(
    row: int, sensors: Iterable[ProximitySensor]
) -> int:
    intervals = list(_intervals_which_cannot_be_beacon(row, sensors))
    return _length_of_union(intervals)
