from itertools import combinations
from typing import Iterator

from models.common.vectors import CardinalDirection, Vector2D


class KeypadLayout:
    def __init__(self, button_positions: dict[chr, Vector2D]) -> None:
        self._btn_positions = button_positions
        self._available_positions = set(button_positions.values())

    def _is_valid(
        self, path: list[CardinalDirection], start_position: Vector2D
    ) -> bool:
        pos = start_position
        for direction in path:
            pos = pos.move(direction, y_grows_down=True)
            if pos not in self._available_positions:
                return False
        return True

    def shortest_paths_between_buttons(
        self, button_a: chr, button_b: chr
    ) -> Iterator[tuple[CardinalDirection]]:
        pos_a = self._btn_positions[button_a]
        pos_b = self._btn_positions[button_b]
        diff = pos_b - pos_a
        dx = diff.x
        dy = diff.y
        horizontal_step = CardinalDirection.EAST if dx > 0 else CardinalDirection.WEST
        vertical_step = CardinalDirection.SOUTH if dy > 0 else CardinalDirection.NORTH
        slots = [i for i in range(diff.manhattan_size)]
        num_horizontal_steps = abs(dx)
        for choice in combinations(slots, num_horizontal_steps):
            path = [
                horizontal_step if i in choice else vertical_step
                for i in range(diff.manhattan_size)
            ]
            if self._is_valid(path, pos_a):
                yield tuple(path)
