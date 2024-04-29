from typing import Iterator, Hashable, Optional
from models.vectors import Vector2D
from models.cellular_automata.multi_state_automata import (
    Cell,
    CellType,
    MultiStateCellVicinity,
    multi_state_automaton_next_state,
)


class MultiState2DAutomaton:
    def __init__(
        self,
        default_cell_type: Hashable = 0,
        width: Optional[int] = None,
        height: Optional[int] = None,
        consider_diagonal_neighbors: bool = True,
    ) -> None:
        self._default_cell_type = default_cell_type
        self._width = width
        self._height = height
        self._consider_diagonal_neighbors = consider_diagonal_neighbors

    @property
    def default_cell_type(self) -> Hashable:
        return self._default_cell_type

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

    def apply_rule(self, vicinity: MultiStateCellVicinity) -> CellType:
        raise NotImplementedError("Must be implemented by subclass")

    def next_state(self, cells: dict[Vector2D:Hashable]) -> dict[Vector2D:Hashable]:
        return multi_state_automaton_next_state(self, cells)
