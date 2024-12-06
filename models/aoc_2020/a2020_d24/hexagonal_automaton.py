from typing import Iterator

from models.common.cellular_automata import (
    TwoStateCellVicinity,
    two_state_automaton_next_state,
)
from models.common.vectors import CanonicalHexagonalCoordinates


class HexagonalAutomaton:
    @staticmethod
    def is_within_bounds(cell: CanonicalHexagonalCoordinates) -> bool:
        return True

    @staticmethod
    def neighbors(
        cell: CanonicalHexagonalCoordinates,
    ) -> Iterator[CanonicalHexagonalCoordinates]:
        yield from cell.adjacent_positions()

    @staticmethod
    def cell_is_alive_in_next_generation(vicinity: TwoStateCellVicinity) -> bool:
        return (
            not vicinity.center_cell_is_alive and vicinity.num_alive_neighbors() == 2
        ) or (
            vicinity.center_cell_is_alive and 1 <= vicinity.num_alive_neighbors() <= 2
        )

    def next_state(
        self, active_cells: set[CanonicalHexagonalCoordinates]
    ) -> set[CanonicalHexagonalCoordinates]:
        return two_state_automaton_next_state(self, alive_cells=active_cells)
