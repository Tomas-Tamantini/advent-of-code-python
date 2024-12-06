from typing import Optional

from models.common.cellular_automata.two_state_automata import (
    TwoStateCellVicinity,
    two_state_automaton_next_state,
)
from models.common.vectors import Vector2D

from .bounded_2d_automata import Bounded2DAutomaton


class GameOfLife(Bounded2DAutomaton):
    def __init__(
        self, width: Optional[int] = None, height: Optional[int] = None
    ) -> None:
        super().__init__(width, height)

    @staticmethod
    def cell_is_alive_in_next_generation(vicinity: TwoStateCellVicinity) -> bool:
        return (
            not vicinity.center_cell_is_alive and vicinity.num_alive_neighbors() == 3
        ) or (
            vicinity.center_cell_is_alive and 2 <= vicinity.num_alive_neighbors() <= 3
        )

    def next_state(self, live_cells: set[Vector2D]) -> set[Vector2D]:
        return two_state_automaton_next_state(self, live_cells)
