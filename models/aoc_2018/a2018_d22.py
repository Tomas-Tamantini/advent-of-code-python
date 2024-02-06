from typing import Optional
import numpy as np
from models.vectors import Vector2D, BoundingBox


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
        self._erosion_levels = np.zeros((target.y + 1, target.x + 1), dtype=int)
        self._calculate_erosion_levels()

    def _calculate_erosion_levels(self) -> None:
        for y in range(self._erosion_levels.shape[0]):
            for x in range(self._erosion_levels.shape[1]):
                self._erosion_levels[y, x] = self._erosion_level(Vector2D(x, y))

    def _erosion_level(self, pos: Vector2D) -> int:
        if pos == Vector2D(0, 0) or pos == self._target:
            geo_index = 0
        elif pos.y == 0:
            geo_index = pos.x * self._row_multiplier
        elif pos.x == 0:
            geo_index = pos.y * self._col_multiplier
        else:
            geo_index = (
                self._erosion_levels[pos.y, pos.x - 1]
                * self._erosion_levels[pos.y - 1, pos.x]
            )
        return (geo_index + self._depth) % self._erosion_level_mod

    def erosion_level(self, pos: Vector2D) -> int:
        return self._erosion_levels[pos.y, pos.x]

    def risk_level(self, region: Optional[BoundingBox] = None) -> int:
        if region is None:
            region = BoundingBox(
                bottom_left=Vector2D(0, 0),
                top_right=self._target,
            )
        return np.sum(
            self._erosion_levels[
                region.bottom_left.y : region.top_right.y + 1,
                region.bottom_left.x : region.top_right.x + 1,
            ]
            % 3
        )
