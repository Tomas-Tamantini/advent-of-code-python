from typing import Iterator
from models.vectors import VectorNDimensional
from models.cellular_automata import CellCluster, automaton_next_state, GameOfLife


class HyperGameOfLife:
    @property
    def default_cell_type(self) -> int:
        return GameOfLife().default_cell_type

    def is_within_bounds(self, cell: VectorNDimensional) -> bool:
        return True

    def neighbors(self, cell: VectorNDimensional) -> Iterator[VectorNDimensional]:
        yield from cell.adjacent_positions()

    def apply_rule(self, cluster: CellCluster) -> int:
        return GameOfLife().apply_rule(cluster)

    def next_state(
        self, active_cells: set[VectorNDimensional]
    ) -> set[VectorNDimensional]:
        cells = {cell: 1 for cell in active_cells}
        next_cells = automaton_next_state(self, cells)
        return {cell for cell, cell_type in next_cells.items() if cell_type == 1}
