from typing import Callable, Iterator, Protocol

from models.common.number_theory import gcd
from models.common.vectors import Vector2D


class AntinodeGenerator(Protocol):
    def antinodes(
        self,
        pos_a: ValueError,
        pos_b: Vector2D,
        is_within_bounds: Callable[[Vector2D], bool],
    ) -> Iterator[Vector2D]: ...


class TwiceDistanceAntinodeGenerator:
    @staticmethod
    def _all_antinodes(pos_a: Vector2D, pos_b: Vector2D) -> Iterator[Vector2D]:
        yield 2 * pos_a - pos_b
        yield 2 * pos_b - pos_a
        middle_1 = 2 * pos_a + pos_b
        if middle_1.x % 3 == 0 and middle_1.y % 3 == 0:
            yield Vector2D(middle_1.x // 3, middle_1.y // 3)
        middle_2 = pos_a + 2 * pos_b
        if middle_2.x % 3 == 0 and middle_2.y % 3 == 0:
            yield Vector2D(middle_2.x // 3, middle_2.y // 3)

    @staticmethod
    def antinodes(
        pos_a: ValueError,
        pos_b: Vector2D,
        is_within_bounds: Callable[[Vector2D], bool],
    ) -> Iterator[Vector2D]:
        for antinode in TwiceDistanceAntinodeGenerator._all_antinodes(pos_a, pos_b):
            if is_within_bounds(antinode):
                yield antinode


class CollinearAntinodeGenerator:
    @staticmethod
    def _step(pos_a, pos_b):
        diff = pos_b - pos_a
        gcd_diff = gcd(abs(diff.x), abs(diff.y))
        return Vector2D(diff.x // gcd_diff, diff.y // gcd_diff)

    @staticmethod
    def antinodes(
        pos_a: ValueError,
        pos_b: Vector2D,
        is_within_bounds: Callable[[Vector2D], bool],
    ) -> Iterator[Vector2D]:
        delta = CollinearAntinodeGenerator._step(pos_a, pos_b)

        pos = pos_a
        while is_within_bounds(pos):
            yield pos
            pos += delta

        pos = pos_a - delta
        while is_within_bounds(pos):
            yield pos
            pos -= delta
