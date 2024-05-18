from typing import Iterator, Protocol
from collections import defaultdict
from dataclasses import dataclass
from .multi_state_automata import Cell


@dataclass
class TwoStateCellVicinity:
    center_cell: Cell
    center_cell_is_alive: bool
    alive_neighbors: set[Cell]

    def num_alive_neighbors(self) -> int:
        return len(self.alive_neighbors)


class TwoStateAutomaton(Protocol):
    def is_within_bounds(self, cell: Cell) -> bool: ...

    def neighbors(self, cell: Cell) -> Iterator[Cell]: ...

    def cell_is_alive_in_next_generation(
        self, vicinity: TwoStateCellVicinity
    ) -> bool: ...


def two_state_automaton_next_state(
    automaton: TwoStateAutomaton, alive_cells: set[Cell]
) -> set[Cell]:
    all_cells = set()
    neighbors_by_cell = defaultdict(set)
    for cell in alive_cells:
        if automaton.is_within_bounds(cell):
            all_cells.add(cell)
            for neighbor in automaton.neighbors(cell):
                if automaton.is_within_bounds(neighbor):
                    neighbors_by_cell[neighbor].add(cell)
                    all_cells.add(neighbor)

    next_state = set()

    for cell in all_cells:
        vicinity = TwoStateCellVicinity(
            center_cell=cell,
            center_cell_is_alive=cell in alive_cells,
            alive_neighbors=neighbors_by_cell[cell],
        )
        if automaton.cell_is_alive_in_next_generation(vicinity):
            next_state.add(cell)
    return next_state
