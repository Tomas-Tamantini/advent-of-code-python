from typing import Hashable, Optional
from models.vectors import Vector2D
from .multi_state_2d_automata import MultiStateCellVicinity, MultiState2DAutomaton

DEAD, ALIVE = 0, 1


class GameOfLife(MultiState2DAutomaton):
    def __init__(
        self, width: Optional[int] = None, height: Optional[int] = None
    ) -> None:
        default_cell_type = DEAD
        super().__init__(default_cell_type, width, height)

    def apply_rule(self, vicinity: MultiStateCellVicinity) -> Hashable:
        if (
            vicinity.center_cell_type == DEAD
            and vicinity.num_neighbors_by_type(ALIVE) == 3
        ) or (
            vicinity.center_cell_type == ALIVE
            and 2 <= vicinity.num_neighbors_by_type(ALIVE) <= 3
        ):
            return ALIVE
        else:
            return DEAD

    def next_live_cells(self, live_cells: set[Vector2D]) -> set[Vector2D]:
        cells = {pos: ALIVE for pos in live_cells}
        next_gen = self.next_state(cells)
        return {pos for pos, cell in next_gen.items() if cell == ALIVE}
