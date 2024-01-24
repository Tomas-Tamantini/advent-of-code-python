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
        occupied = set(self._seeds)
        cells_to_expand = {s: s for s in self._seeds}
        consolidated_cells = defaultdict(set)
        finite_expansion_cells = set(self._seeds) - set(
            self.seeds_that_extend_indefinetely()
        )
        while set(cells_to_expand.values()) & finite_expansion_cells:
            new_cells_to_expand = dict()
            for position, seed in cells_to_expand.items():
                if seed is not None:
                    consolidated_cells[seed].add(position)
                for new_position in position.adjacent_positions():
                    if new_position in occupied:
                        continue
                    if new_position not in new_cells_to_expand:
                        new_cells_to_expand[new_position] = seed
                    elif new_cells_to_expand[new_position] != seed:
                        new_cells_to_expand[new_position] = None
            cells_to_expand = new_cells_to_expand
            for position in cells_to_expand:
                occupied.add(position)
        return {
            s: len(consolidated_cells[s]) if s in finite_expansion_cells else inf
            for s in self._seeds
        }
