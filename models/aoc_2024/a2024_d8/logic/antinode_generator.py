from typing import Callable, Iterator, Protocol

from models.common.vectors import Vector2D


class AntinodeGenerator(Protocol):
    def antinodes(
        self,
        pos_a: ValueError,
        pos_b: Vector2D,
        is_within_bounds: Callable[[Vector2D], bool],
    ) -> Iterator[Vector2D]: ...


class TwiceDistanceAntinodeGenerator:
    def _all_antinodes(self, pos_a: Vector2D, pos_b: Vector2D) -> Iterator[Vector2D]:
        yield 2 * pos_a - pos_b
        yield 2 * pos_b - pos_a
        middle_1 = 2 * pos_a + pos_b
        if middle_1.x % 3 == 0 and middle_1.y % 3 == 0:
            yield Vector2D(middle_1.x // 3, middle_1.y // 3)
        middle_2 = pos_a + 2 * pos_b
        if middle_2.x % 3 == 0 and middle_2.y % 3 == 0:
            yield Vector2D(middle_2.x // 3, middle_2.y // 3)

    def antinodes(
        self,
        pos_a: ValueError,
        pos_b: Vector2D,
        is_within_bounds: Callable[[Vector2D], bool],
    ) -> Iterator[Vector2D]:
        for antinode in self._all_antinodes(pos_a, pos_b):
            if is_within_bounds(antinode):
                yield antinode
