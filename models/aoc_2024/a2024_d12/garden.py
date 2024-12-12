from dataclasses import dataclass
from typing import Iterator

from models.common.graphs import DisjointSet
from models.common.io import CharacterGrid
from models.common.vectors import CardinalDirection, Vector2D


@dataclass(frozen=True)
class GardenRegion:
    area: int
    perimeter: int

    def increment(self, other: "GardenRegion") -> "GardenRegion":
        return GardenRegion(self.area + other.area, self.perimeter + other.perimeter)


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
        _regions = dict()
        for position in self._positions():
            root = disjoint_set.find(position)
            if root not in _regions:
                _regions[root] = GardenRegion(0, 0)
            area_increment = 1
            perimeter_increment = 0
            for neighbor in position.adjacent_positions():
                if not self._grid.contains(neighbor):
                    perimeter_increment += 1
                elif disjoint_set.find(neighbor) != root:
                    perimeter_increment += 1
            _regions[root] = _regions[root].increment(
                GardenRegion(area_increment, perimeter_increment)
            )
        yield from _regions.values()
