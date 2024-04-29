from typing import Iterator
from models.vectors import CanonicalHexagonalCoordinates
from models.cellular_automata import (
    MultiStateCellVicinity,
    multi_state_automaton_next_state,
)

WHITE = 0
BLACK = 1


class HexagonalAutomaton:
    @property
    def default_cell_type(self) -> int:
        return WHITE

    def is_within_bounds(self, cell: CanonicalHexagonalCoordinates) -> bool:
        return True

    def neighbors(
        self, cell: CanonicalHexagonalCoordinates
    ) -> Iterator[CanonicalHexagonalCoordinates]:
        yield from cell.adjacent_positions()

    def apply_rule(self, vicinity: MultiStateCellVicinity) -> int:
        if (
            vicinity.center_cell_type == WHITE
            and vicinity.num_neighbors_by_type(BLACK) == 2
        ) or (
            vicinity.center_cell_type == BLACK
            and 1 <= vicinity.num_neighbors_by_type(BLACK) <= 2
        ):
            return BLACK
        else:
            return WHITE

    def next_state(
        self, active_cells: set[CanonicalHexagonalCoordinates]
    ) -> set[CanonicalHexagonalCoordinates]:
        cells = {cell: BLACK for cell in active_cells}
        next_cells = multi_state_automaton_next_state(self, cells)
        return {cell for cell, cell_type in next_cells.items() if cell_type == BLACK}
