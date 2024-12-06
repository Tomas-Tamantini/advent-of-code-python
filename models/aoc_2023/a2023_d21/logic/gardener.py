from typing import Iterable, Iterator

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
        current_iteration_is_even = True
        even_iteration_positions = set()
        odd_iteration_positions = set()
        current_positions = {self._initial_position}
        while True:
            if current_iteration_is_even:
                even_iteration_positions.update(current_positions)
                yield len(even_iteration_positions)
            else:
                odd_iteration_positions.update(current_positions)
                yield len(odd_iteration_positions)

            next_positions = set()
            for next_pos in self._next_positions(current_positions, garden):
                if (next_pos not in even_iteration_positions) and (
                    next_pos not in odd_iteration_positions
                ):
                    next_positions.add(next_pos)

            current_positions = next_positions
            current_iteration_is_even = not current_iteration_is_even
