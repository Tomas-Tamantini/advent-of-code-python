from collections import defaultdict
from itertools import combinations
from typing import Iterator

from models.common.vectors import Vector2D

from .antenna import Antenna
from .antinode_generator import AntinodeGenerator


class AntennaRange:
    def __init__(self, width: int, height: int, antennas: set[Antenna]):
        self._width = width
        self._height = height
        self._antenna_positions = defaultdict(set)
        for antenna in antennas:
            self._antenna_positions[antenna.frequency].add(antenna.position)

    def _is_within_bounds(self, position: Vector2D) -> bool:
        return 0 <= position.x < self._width and 0 <= position.y < self._height

    def antinodes(self, antinode_generator: AntinodeGenerator) -> Iterator[Vector2D]:
        for positions in self._antenna_positions.values():
            for pair in combinations(positions, 2):
                yield from antinode_generator.antinodes(*pair, self._is_within_bounds)
