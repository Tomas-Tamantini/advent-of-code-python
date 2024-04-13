from typing import Hashable

from models.vectors import Vector2D
from models.cellular_automata import CellCluster, MultiState2DAutomaton

DEAD, ALIVE = 0, 1


class BugsAutomaton(MultiState2DAutomaton):
    def __init__(self, width: int, height: int) -> None:
        default_cell_type = DEAD
        super().__init__(
            default_cell_type, width, height, consider_diagonal_neighbors=False
        )

    def _apply_rule(self, cluster: CellCluster) -> Hashable:
        if cluster.cell_type == DEAD and 1 <= cluster.neighbors.count(ALIVE) <= 2:
            return ALIVE
        elif cluster.cell_type == ALIVE and cluster.neighbors.count(ALIVE) == 1:
            return ALIVE
        return DEAD

    def next_live_cells(self, live_cells: set[Vector2D]) -> set[Vector2D]:
        cells = {c: ALIVE for c in live_cells}
        next_gen = self.next_state(cells)
        return {pos for pos, cell in next_gen.items() if cell == ALIVE}

    def biodiversity_rating(self, live_cells: set[Vector2D]) -> int:
        return sum(2 ** (c.y * self._width + c.x) for c in live_cells)

    def first_pattern_to_appear_twice(
        self, initial_configuration: set[Vector2D]
    ) -> set[Vector2D]:
        seen = set()
        state = initial_configuration
        while True:
            if frozenset(state) in seen:
                return state
            seen.add(frozenset(state))
            state = self.next_live_cells(state)

    def render(self, live_cells: set[Vector2D]) -> str:
        return "\n".join(
            "".join(
                "#" if Vector2D(x, y) in live_cells else "." for x in range(self._width)
            )
            for y in range(self._height)
        )
