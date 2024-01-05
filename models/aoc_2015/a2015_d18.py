from collections import defaultdict
from typing import Iterator


class GameOfLife:
    def __init__(self, grid_width: int, grid_height: int) -> None:
        self._width = grid_width
        self._height = grid_height

    def _is_within_bounds(self, cell: tuple[int, int]) -> bool:
        return 0 <= cell[0] < self._width and 0 <= cell[1] < self._height

    def _neighbors(self, cell: tuple[int, int]) -> Iterator[tuple[int, int]]:
        x, y = cell
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbor = x + dx, y + dy
                if neighbor != cell and self._is_within_bounds(neighbor):
                    yield neighbor

    def step(self, live_cells: set[tuple[int, int]]) -> set[tuple[int, int]]:
        num_live_neighbors: defaultdict[tuple[int, int], int] = defaultdict(int)
        for cell in live_cells:
            for neighbor in self._neighbors(cell):
                num_live_neighbors[neighbor] += 1

        next_live_cells = set()
        for cell, num_neighbors in num_live_neighbors.items():
            if num_neighbors == 3 or (num_neighbors == 2 and cell in live_cells):
                next_live_cells.add(cell)

        return next_live_cells
