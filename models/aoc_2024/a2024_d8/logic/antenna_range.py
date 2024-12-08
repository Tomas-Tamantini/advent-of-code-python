from collections import defaultdict
from itertools import combinations
from typing import Iterator

from models.common.vectors import Vector2D

from .antenna import Antenna


class AntennaRange:
    def __init__(self, width: int, height: int, antennas: set[Antenna]):
        self._width = width
        self._height = height
        self._antennas = defaultdict(set)
        for antenna in antennas:
            self._antennas[antenna.frequency].add(antenna)

    def _is_within_bounds(self, position: Vector2D) -> bool:
        return 0 <= position.x < self._width and 0 <= position.y < self._height

    @staticmethod
    def _antinodes_for_pair(pos_a: Vector2D, pos_b: Vector2D) -> Iterator[Vector2D]:
        yield 2 * pos_a - pos_b
        yield 2 * pos_b - pos_a
        middle_1 = 2 * pos_a + pos_b
        if middle_1.x % 3 == 0 and middle_1.y % 3 == 0:
            yield Vector2D(middle_1.x // 3, middle_1.y // 3)
        middle_2 = pos_a + 2 * pos_b
        if middle_2.x % 3 == 0 and middle_2.y % 3 == 0:
            yield Vector2D(middle_2.x // 3, middle_2.y // 3)

    def _antinodes_for_frequency(self, frequency: str) -> Iterator[Vector2D]:
        antennas = self._antennas[frequency]
        for a_1, a_2 in combinations(antennas, 2):
            for antinode in self._antinodes_for_pair(a_1.position, a_2.position):
                if self._is_within_bounds(antinode):
                    yield antinode

    def antinodes(self) -> Iterator[Vector2D]:
        for frequency in self._antennas:
            yield from self._antinodes_for_frequency(frequency)
