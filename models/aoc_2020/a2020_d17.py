from typing import Iterator
from models.vectors import Vector3D
from models.cellular_automata import CellCluster, automaton_next_state

INACTIVE = 0
ACTIVE = 1


class CellularAutomaton3D:
    @property
    def default_cell_type(self) -> int:
        return INACTIVE

    def is_within_bounds(self, cell: Vector3D) -> bool:
        return True

    def neighbors(self, cell: Vector3D) -> Iterator[Vector3D]:
        yield from cell.adjacent_positions()

    def apply_rule(self, cluster: CellCluster) -> int:
        if cluster.cell_type == ACTIVE:
            return (
                ACTIVE if 2 <= cluster.num_neighbors_by_type[ACTIVE] <= 3 else INACTIVE
            )
        else:
            return ACTIVE if cluster.num_neighbors_by_type[ACTIVE] == 3 else INACTIVE

    def next_state(self, active_cells: set[Vector3D]) -> set[Vector3D]:
        cells = {cell: ACTIVE for cell in active_cells}
        next_cells = automaton_next_state(self, cells)
        return {cell for cell, cell_type in next_cells.items() if cell_type == ACTIVE}
