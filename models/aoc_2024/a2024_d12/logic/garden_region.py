from dataclasses import dataclass

from models.common.vectors import Vector2D


@dataclass(frozen=True)
class _GardenRegionDimensions:
    area: int
    perimeter: int


class GardenRegion:
    def __init__(self, positions: set[Vector2D]):
        self._positions = positions

    def dimensions(self) -> _GardenRegionDimensions:
        perimeter = 0
        for pos in self._positions:
            for neighbor in pos.adjacent_positions():
                if neighbor not in self._positions:
                    perimeter += 1
        return _GardenRegionDimensions(len(self._positions), perimeter)
