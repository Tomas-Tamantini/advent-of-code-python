from enum import Enum
from math import inf
from typing import Iterator, Optional

from models.common.cellular_automata import (
    MultiStateCellVicinity,
    multi_state_automaton_next_state,
)
from models.common.io import ProgressBar
from models.common.vectors import Vector2D


class _CellType(int, Enum):
    LIT = 1
    UNLIT = 2
    DEFAULT = 3


class TrenchMapAutomaton:
    def __init__(self, lit_cell_configurations: set[int]) -> None:
        self._lit_cell_configurations = lit_cell_configurations
        self._iteration = 0

    @property
    def default_cell_type(self) -> _CellType:
        return _CellType.DEFAULT

    def is_within_bounds(self, cell: Vector2D) -> bool:
        return True

    def neighbors(self, cell: Vector2D) -> Iterator[Vector2D]:
        for neighbor in cell.adjacent_positions(include_diagonals=True):
            yield neighbor

    def _cell_is_lit(self, cell_type: _CellType) -> bool:
        if cell_type == _CellType.LIT:
            return True
        elif cell_type == _CellType.UNLIT:
            return False
        else:
            return self._lit_is_the_default_type(self._iteration)

    def apply_rule(self, vicinity: MultiStateCellVicinity) -> _CellType:
        configuration = 0
        for row in range(-1, 2):
            for col in range(-1, 2):
                configuration <<= 1
                if row == col == 0:
                    if self._cell_is_lit(vicinity.center_cell_type):
                        configuration |= 1
                else:
                    neighbor = vicinity.center_cell + Vector2D(col, row)
                    neighbor_type = vicinity.neighbors.get(neighbor, _CellType.DEFAULT)
                    if self._cell_is_lit(neighbor_type):
                        configuration |= 1

        return (
            _CellType.LIT
            if configuration in self._lit_cell_configurations
            else _CellType.UNLIT
        )

    def next_state(
        self, lit_cells: dict[Vector2D:_CellType]
    ) -> dict[Vector2D:_CellType]:
        return multi_state_automaton_next_state(self, lit_cells)

    def _lit_is_the_default_type(self, num_steps: int) -> bool:
        return (
            0 in self._lit_cell_configurations
            and num_steps > 0
            and ((num_steps % 2 == 1) or (511 in self._lit_cell_configurations))
        )

    def num_lit_cells_after(
        self,
        num_steps: int,
        initial_lit_cells: set[Vector2D],
        progress_bar: Optional[ProgressBar] = None,
    ) -> int:
        if self._lit_is_the_default_type(num_steps):
            return inf
        self._iteration = 0
        state = {cell: _CellType.LIT for cell in initial_lit_cells}
        for _ in range(num_steps):
            state = self.next_state(state)
            self._iteration += 1
            if progress_bar:
                progress_bar.update(self._iteration, num_steps)
        lit_cells = {c for c, status in state.items() if status == _CellType.LIT}
        return len(lit_cells)
