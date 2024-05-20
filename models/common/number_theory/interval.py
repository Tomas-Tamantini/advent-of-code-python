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
