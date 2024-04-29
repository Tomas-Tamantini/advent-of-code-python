from typing import Iterator
from models.cellular_automata import GameOfLife
from models.vectors import Vector2D


class GameOfLifeLights(GameOfLife):
    def __init__(self, grid_width: int, grid_height: int) -> None:
        super().__init__(grid_width, grid_height)

    @property
    def corner_cells(self) -> Iterator[Vector2D]:
        yield Vector2D(0, 0)
        yield Vector2D(self._width - 1, 0)
        yield Vector2D(0, self._height - 1)
        yield Vector2D(self._width - 1, self._height - 1)

    def step_with_always_on_cells(
        self, live_cells: set[Vector2D], always_on_cells: set[Vector2D]
    ) -> set[Vector2D]:
        actual_live_cells = live_cells | always_on_cells
        next_live_cells = self.next_state(actual_live_cells)
        return next_live_cells | always_on_cells
