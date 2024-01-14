from collections import defaultdict
from typing import Iterator, Optional


class GameOfLife:
    def __init__(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
    ) -> None:
        self._width = width
        self._height = height

    def _is_within_bounds(self, x: int, y: int) -> bool:
        if self._width is None or self._height is None:
            return True
        return 0 <= x < self._width and 0 <= y < self._height

    def _neighbors(self, x: int, y: int) -> Iterator[tuple[int, int]]:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                new_x, new_y = x + dx, y + dy
                if (new_x, new_y) != (x, y) and self._is_within_bounds(new_x, new_y):
                    yield new_x, new_y

    def _num_live_neighbors(
        self, live_cells: set[tuple[int, int]]
    ) -> dict[tuple[int, int], int]:
        num_live_neighbors: defaultdict[tuple[int, int], int] = defaultdict(int)
        for cell in live_cells:
            for neighbor in self._neighbors(*cell):
                num_live_neighbors[neighbor] += 1
        return num_live_neighbors

    def next_state(self, live_cells: set[tuple[int, int]]) -> set[tuple[int, int]]:
        next_live_cells = set()
        for cell, num_neighbors in self._num_live_neighbors(live_cells).items():
            if num_neighbors == 3 or (num_neighbors == 2 and cell in live_cells):
                next_live_cells.add(cell)

        return next_live_cells
