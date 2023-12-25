from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class XmasPresent:
    width: int
    height: int
    length: int

    def side_areas(self) -> Iterator[int]:
        yield self.width * self.height
        yield self.height * self.length
        yield self.length * self.width

    def side_perimeters(self) -> Iterator[int]:
        yield 2 * (self.width + self.height)
        yield 2 * (self.height + self.length)
        yield 2 * (self.length + self.width)

    def area_required_to_wrap(self) -> int:
        side_areas = list(self.side_areas())
        return sum(side_areas) * 2 + min(side_areas)

    def ribbon_required_to_wrap(self) -> int:
        side_perimeters = list(self.side_perimeters())
        return min(side_perimeters) + self.width * self.height * self.length
