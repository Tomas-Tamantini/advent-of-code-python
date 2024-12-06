from typing import Iterator

from models.common.vectors import CardinalDirection, Vector2D

from .rope_knot import RopeKnot


class Rope:
    def __init__(self, num_knots: int) -> None:
        self._knots_head_to_tail = [
            RopeKnot(position=Vector2D(0, 0)) for _ in range(num_knots)
        ]

    def positions_head_to_tail(self) -> Iterator[Vector2D]:
        return (knot.position for knot in self._knots_head_to_tail)

    @property
    def tail_position(self) -> Vector2D:
        return self._knots_head_to_tail[-1].position

    def move_head(self, direction: CardinalDirection) -> None:
        self._knots_head_to_tail[0] = self._knots_head_to_tail[0].move(direction)
        for i in range(1, len(self._knots_head_to_tail)):
            self._knots_head_to_tail[i] = self._knots_head_to_tail[i - 1].pull(
                self._knots_head_to_tail[i]
            )
