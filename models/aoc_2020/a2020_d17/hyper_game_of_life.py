from typing import Iterator

from models.common.cellular_automata import (
    GameOfLife,
    TwoStateCellVicinity,
    two_state_automaton_next_state,
)
from models.common.vectors import VectorNDimensional


class HyperGameOfLife:
    def is_within_bounds(self, cell: VectorNDimensional) -> bool:
        return True

    def neighbors(self, cell: VectorNDimensional) -> Iterator[VectorNDimensional]:
        yield from cell.adjacent_positions()

    def cell_is_alive_in_next_generation(self, vicinity: TwoStateCellVicinity) -> bool:
        return GameOfLife().cell_is_alive_in_next_generation(vicinity)

    def next_state(
        self, active_cells: set[VectorNDimensional]
    ) -> set[VectorNDimensional]:
        return two_state_automaton_next_state(self, active_cells)
