from typing import Iterator, Iterable
from models.common.vectors import Vector2D
from .garden import Garden


class Gardener:
    def __init__(self, initial_position: Vector2D) -> None:
        self._initial_position = initial_position

    def _valid_neighbors(
        self, position: Vector2D, garden: Garden
    ) -> Iterator[Vector2D]:
        for neighbor in position.adjacent_positions():
            if garden.is_valid_position(neighbor):
                yield neighbor

    def _next_positions(
        self, current_positions: Iterable[Vector2D], garden: Garden
    ) -> Iterator[Vector2D]:
        for pos in current_positions:
            yield from self._valid_neighbors(pos, garden)

    def num_reachable_positions(self, garden: Garden) -> Iterator[int]:
        current_positions = {self._initial_position}
        while True:
            yield len(current_positions)
            current_positions = set(self._next_positions(current_positions, garden))
