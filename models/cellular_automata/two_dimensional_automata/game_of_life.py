from typing import Hashable, Optional

from models.vectors import Vector2D
from .multi_state_automata import CellCluster, MultiState2DAutomaton

DEAD, ALIVE = 0, 1


class GameOfLife(MultiState2DAutomaton):
    def __init__(
        self, width: Optional[int] = None, height: Optional[int] = None
    ) -> None:
        default_cell_type = DEAD
        super().__init__(default_cell_type, width, height)

    def _apply_rule(self, cluster: CellCluster) -> Hashable:
        if cluster.cell_type == DEAD and cluster.neighbors.count(ALIVE) == 3:
            return ALIVE
        elif cluster.cell_type == ALIVE and 2 <= cluster.neighbors.count(ALIVE) <= 3:
            return ALIVE
        return DEAD

    def next_live_cells(self, live_cells: set[tuple[int, int]]) -> set[tuple[int, int]]:
        cells = {Vector2D(x, y): ALIVE for x, y in live_cells}
        next_gen = self.next_state(cells)
        return {(pos.x, pos.y) for pos, cell in next_gen.items() if cell == ALIVE}
