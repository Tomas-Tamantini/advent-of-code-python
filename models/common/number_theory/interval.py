from dataclasses import dataclass
from typing import Iterator, Optional


@dataclass(frozen=True, order=True)
class Interval:
    min_inclusive: int
    max_inclusive: int

    @property
    def num_elements(self) -> int:
        return self.max_inclusive - self.min_inclusive + 1

    def contains(self, number: int) -> bool:
        return self.min_inclusive <= number <= self.max_inclusive

    def intersection(self, other: "Interval") -> Optional["Interval"]:
        new_min = max(self.min_inclusive, other.min_inclusive)
        new_max = min(self.max_inclusive, other.max_inclusive)
        if new_min > new_max:
            return None
        else:
            return Interval(min_inclusive=new_min, max_inclusive=new_max)

    def is_contained_by(self, other: "Interval") -> bool:
        return self == self.intersection(other)

    def offset(self, offset: int) -> "Interval":
        return Interval(
            min_inclusive=self.min_inclusive + offset,
            max_inclusive=self.max_inclusive + offset,
        )

    def __sub__(self, other: "Interval") -> Iterator["Interval"]:
        intersection = self.intersection(other)
        if intersection is None:
            yield self
        else:
            left_min = self.min_inclusive
            left_max = intersection.min_inclusive - 1
            if left_min <= left_max:
                yield Interval(min_inclusive=left_min, max_inclusive=left_max)

            right_min = intersection.max_inclusive + 1
            right_max = self.max_inclusive
            if right_min <= right_max:
                yield Interval(min_inclusive=right_min, max_inclusive=right_max)
