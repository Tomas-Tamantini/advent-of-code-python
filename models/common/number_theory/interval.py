from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
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
