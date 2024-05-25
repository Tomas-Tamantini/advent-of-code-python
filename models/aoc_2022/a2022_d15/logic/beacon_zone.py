from typing import Iterable, Iterator, Optional
from models.common.number_theory import Interval
from models.common.vectors import BoundingBox, Vector2D
from .proximity_sensor import ProximitySensor


def _intervals_which_cannot_be_unknown_beacon(
    row: int, sensors: Iterable[ProximitySensor]
) -> Iterator[Interval]:
    for sensor in sensors:
        interval = sensor.interval_which_cannot_be_unknown_beacon(row)
        if interval is not None:
            yield interval


def _position_which_must_be_beacon(
    search_inverval: Interval, intervals_to_eliminate: Iterable[Interval]
) -> Optional[int]:
    sorted_intervals = sorted(intervals_to_eliminate)
    if (
        not sorted_intervals
        or sorted_intervals[0].min_inclusive > search_inverval.min_inclusive
    ):
        return search_inverval.min_inclusive
    current_end = sorted_intervals[0].max_inclusive
    for interval in sorted_intervals[1:]:
        if current_end >= search_inverval.max_inclusive:
            return None
        elif interval.min_inclusive > current_end + 1:
            return current_end + 1
        else:
            current_end = max(current_end, interval.max_inclusive)
    if current_end < search_inverval.max_inclusive:
        return max(current_end + 1, search_inverval.min_inclusive)


def position_which_must_be_beacon(
    search_space: BoundingBox, sensors: Iterable[ProximitySensor]
) -> Vector2D:
    search_interval = Interval(search_space.min_x, search_space.max_x + 1)
    for row in range(search_space.min_y, search_space.max_y + 1):
        print(row)
        column = _position_which_must_be_beacon(
            search_interval, _intervals_which_cannot_be_unknown_beacon(row, sensors)
        )
        if column is not None:
            return Vector2D(column, row)
