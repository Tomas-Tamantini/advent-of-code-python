from typing import Iterator, Optional

from models.common.cellular_automata.multi_state_automata import Cell
from models.common.vectors import Vector2D


class Bounded2DAutomaton:
    def __init__(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        consider_diagonal_neighbors: bool = True,
    ) -> None:
        self._width = width
        self._height = height
        self._consider_diagonal_neighbors = consider_diagonal_neighbors

    @property
    def width(self) -> Optional[int]:
        return self._width

    @property
    def height(self) -> Optional[int]:
        return self._height

    def is_within_bounds(self, cell: Vector2D) -> bool:
        if self._width is None or self._height is None:
            return True
        return 0 <= cell.x < self._width and 0 <= cell.y < self._height

    def neighbors(self, cell: Vector2D) -> Iterator[Cell]:
        for neighbor in cell.adjacent_positions(
            include_diagonals=self._consider_diagonal_neighbors
        ):
            if self.is_within_bounds(neighbor):
                yield neighbor
