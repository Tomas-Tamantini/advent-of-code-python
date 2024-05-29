from typing import Iterator
from bisect import bisect_left, bisect_right


class DisjoinIntervals:
    def __init__(self, interval_start: int, interval_end: int):
        self._intervals = [interval_start, interval_end]

    def intervals(self) -> Iterator[tuple[int, int]]:
        for i in range(0, len(self._intervals), 2):
            yield self._intervals[i], self._intervals[i + 1]

    def num_elements(self) -> int:
        return sum(end - start + 1 for start, end in self.intervals())

    def remove(self, interval_start: int, interval_end: int) -> None:
        """Remove the interval [interval_start, interval_end] from the original interval"""
        start_index = bisect_left(self._intervals, interval_start)
        end_index = bisect_right(self._intervals, interval_end)

        new_left = self._intervals[:start_index]
        new_right = self._intervals[end_index:]

        if len(new_left) % 2 == 1:
            new_left.append(interval_start - 1)
        if len(new_right) % 2 == 1:
            new_right.insert(0, interval_end + 1)
        self._intervals = new_left + new_right
