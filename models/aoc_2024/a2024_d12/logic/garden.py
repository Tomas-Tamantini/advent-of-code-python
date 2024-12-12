from collections import defaultdict
from typing import Iterator

from models.common.graphs import DisjointSet
from models.common.io import CharacterGrid
from models.common.vectors import CardinalDirection, Vector2D

from .garden_region import GardenRegion


class Garden:
    def __init__(self, grid: CharacterGrid):
        self._grid = grid

    def _positions(self) -> Iterator[Vector2D]:
        for x in range(self._grid.width):
            for y in range(self._grid.height):
                yield Vector2D(x, y)

    def _merged_regions(self) -> DisjointSet:
        disjoint_set = DisjointSet()
        for position in self._positions():
            disjoint_set.make_set(position)
            for direction in (CardinalDirection.WEST, CardinalDirection.NORTH):
                neighbor = position.move(direction, y_grows_down=True)
                if self._grid.contains(neighbor) and (
                    self._grid.tiles[position] == self._grid.tiles[neighbor]
                ):
                    disjoint_set.union(position, neighbor)
        return disjoint_set

    def regions(self) -> Iterator[GardenRegion]:
        disjoint_set = self._merged_regions()
        _region_positions = defaultdict(set)
        for position in self._positions():
            root = disjoint_set.find(position)
            _region_positions[root].add(position)
        for positions in _region_positions.values():
            yield GardenRegion(positions)
