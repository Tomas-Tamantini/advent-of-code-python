from typing import Iterator
from models.vectors import Vector2D
from models.cellular_automata import (
    two_state_automaton_next_state,
    TwoStateCellVicinity,
)


class TrenchMapAutomaton:
    def __init__(self, lit_cell_configurations: set[int]) -> None:
        self._live_cell_configurations = lit_cell_configurations

    def is_within_bounds(self, cell: Vector2D) -> bool:
        return True

    def neighbors(self, cell: Vector2D) -> Iterator[Vector2D]:
        for neighbor in cell.adjacent_positions(include_diagonals=True):
            yield neighbor

    def cell_is_alive_in_next_generation(self, vicinity: TwoStateCellVicinity) -> bool:
        configuration = 0
        for row in range(-1, 2):
            for col in range(-1, 2):
                configuration <<= 1
                if row == col == 0:
                    if vicinity.center_cell_is_alive:
                        configuration |= 1
                else:
                    neighbor = vicinity.center_cell + Vector2D(col, row)
                    if neighbor in vicinity.alive_neighbors:
                        configuration |= 1

        return configuration in self._live_cell_configurations

    def next_state(self, live_cells: set[Vector2D]) -> set[Vector2D]:
        return two_state_automaton_next_state(self, live_cells)

    def num_lit_cells_after(self, num_steps: int, initial_state: set[Vector2D]) -> int:
        state = initial_state
        for _ in range(num_steps):
            state = self.next_state(state)
        return len(state)
