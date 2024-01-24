from typing import Iterator
from math import inf
from collections import defaultdict
from models.vectors import Vector2D, CardinalDirection


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

    def areas_after_expansion(self) -> dict[Vector2D, int]:
        min_x = min(s.x for s in self._seeds)
        max_x = max(s.x for s in self._seeds)
        min_y = min(s.y for s in self._seeds)
        max_y = max(s.y for s in self._seeds)
        areas = defaultdict(int)
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                min_dist = inf
                closest_seed = None
                for seed in self._seeds:
                    dist = abs(seed.x - x) + abs(seed.y - y)
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
