from typing import Optional
from enum import Enum
from models.vectors import Vector2D, CardinalDirection, BoundingBox


class RegionType(int, Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2


class RockyCave:
    def __init__(
        self,
        depth: int,
        target: Vector2D,
        row_multiplier: int,
        col_multiplier: int,
        erosion_level_mod: int,
    ) -> None:
        self._depth = depth
        self._target = target
        self._row_multiplier = row_multiplier
        self._col_multiplier = col_multiplier
        self._erosion_level_mod = erosion_level_mod
        self._erosion_levels: dict[Vector2D, int] = dict()

    def erosion_level(self, pos: Vector2D) -> int:
        if pos in self._erosion_levels:
            return self._erosion_levels[pos]
        if pos == Vector2D(0, 0) or pos == self._target:
            geo_index = 0
        elif pos.y == 0:
            geo_index = pos.x * self._row_multiplier
        elif pos.x == 0:
            geo_index = pos.y * self._col_multiplier
        else:
            geo_index = self.erosion_level(
                pos.move(CardinalDirection.WEST)
            ) * self.erosion_level(pos.move(CardinalDirection.SOUTH))
        level = (geo_index + self._depth) % self._erosion_level_mod
        self._erosion_levels[pos] = level
        return level

    def region_type(self, pos: Vector2D) -> RegionType:
        return RegionType(self.erosion_level(pos) % 3)

    def risk_level(self, region: Optional[BoundingBox] = None) -> int:
        if region is None:
            region = BoundingBox(
                bottom_left=Vector2D(0, 0),
                top_right=self._target,
            )
        return sum(
            self.region_type(Vector2D(x, y))
            for x in range(region.bottom_left.x, region.top_right.x + 1)
            for y in range(region.bottom_left.y, region.top_right.y + 1)
        )
