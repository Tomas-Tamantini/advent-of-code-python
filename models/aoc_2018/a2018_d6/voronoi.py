from typing import Iterator, Optional
from math import inf
from collections import defaultdict
from models.common.vectors import Vector2D, CardinalDirection, BoundingBox
from models.common.io import ProgressBar


class ManhattanVoronoi:
    def __init__(self, seeds: list[Vector2D]) -> None:
        self._seeds = seeds

    def seeds_that_extend_indefinetely(self) -> Iterator[Vector2D]:
        open_quadrants = {s: set(CardinalDirection) for s in self._seeds}
        for i in range(len(self._seeds)):
            for j in range(i + 1, len(self._seeds)):
                dx = self._seeds[i].x - self._seeds[j].x
                dy = self._seeds[i].y - self._seeds[j].y
                if dy >= abs(dx):
                    open_quadrants[self._seeds[i]].discard(CardinalDirection.NORTH)
                    open_quadrants[self._seeds[j]].discard(CardinalDirection.SOUTH)
                if dy <= -abs(dx):
                    open_quadrants[self._seeds[i]].discard(CardinalDirection.SOUTH)
                    open_quadrants[self._seeds[j]].discard(CardinalDirection.NORTH)
                if dx >= abs(dy):
                    open_quadrants[self._seeds[i]].discard(CardinalDirection.EAST)
                    open_quadrants[self._seeds[j]].discard(CardinalDirection.WEST)
                if dx <= -abs(dy):
                    open_quadrants[self._seeds[i]].discard(CardinalDirection.WEST)
                    open_quadrants[self._seeds[j]].discard(CardinalDirection.EAST)
            if open_quadrants[self._seeds[i]]:
                yield self._seeds[i]

    def _bounding_box(self) -> tuple[int, int, int, int]:
        bounding_box = BoundingBox.from_points(self._seeds)
        return (
            bounding_box.bottom_left.x,
            bounding_box.bottom_left.y,
            bounding_box.top_right.x,
            bounding_box.top_right.y,
        )

    def areas_after_expansion(self) -> dict[Vector2D, int]:
        min_x, min_y, max_x, max_y = self._bounding_box()
        areas = defaultdict(int)
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                min_dist = inf
                closest_seed = None
                for seed in self._seeds:
                    dist = seed.manhattan_distance(Vector2D(x, y))
                    if dist < min_dist:
                        min_dist = dist
                        closest_seed = seed
                    elif dist == min_dist:
                        closest_seed = None
                if closest_seed is not None:
                    areas[closest_seed] += 1
        return {
            s: areas[s] if s not in self.seeds_that_extend_indefinetely() else inf
            for s in self._seeds
        }

    def num_points_whose_sum_of_distances_is_less_than(
        self, max_distance: int, progress_bar: Optional[ProgressBar] = None
    ) -> int:
        radius = max_distance // len(self._seeds)
        min_x, min_y, max_x, max_y = self._bounding_box()
        num_points = 0
        num_steps = (max_x - min_x + 2 * radius + 1) * (max_y - min_y + 2 * radius + 1)
        current_step = 0
        for x in range(min_x - radius, max_x + radius + 1):
            for y in range(min_y - radius, max_y + radius + 1):
                if progress_bar is not None:
                    current_step += 1
                    progress_bar.update(current_step, num_steps)
                if (
                    sum(seed.manhattan_distance(Vector2D(x, y)) for seed in self._seeds)
                    < max_distance
                ):
                    num_points += 1

        return num_points
