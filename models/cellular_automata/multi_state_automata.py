from typing import Iterator, Hashable, Protocol
from collections import defaultdict
from dataclasses import dataclass


Cell = Hashable
CellType = Hashable


@dataclass
class MultiStateCellVicinity:
    center_cell: Cell
    center_cell_type: CellType
    neighbors: dict[Cell:CellType]

    def num_neighbors_by_type(self, cell_type: CellType) -> int:
        return sum(
            1 for neighbor_type in self.neighbors.values() if neighbor_type == cell_type
        )

    def has_at_least_one_neighbor_of_type(self, cell_type: CellType) -> bool:
        return any(
            neighbor_type == cell_type for neighbor_type in self.neighbors.values()
        )


class MultiStateAutomaton(Protocol):
    @property
    def default_cell_type(self) -> CellType: ...

    def is_within_bounds(self, cell: Cell) -> bool: ...

    def neighbors(self, cell: Cell) -> Iterator[Cell]: ...

    def apply_rule(self, vicinity: MultiStateCellVicinity) -> CellType: ...


def multi_state_automaton_next_state(
    automaton: MultiStateAutomaton, cells: dict[Cell:CellType]
) -> dict[Cell:CellType]:
    all_cells = set()
    neighbors_by_cell = defaultdict(dict)
    for cell, cell_type in cells.items():
        if automaton.is_within_bounds(cell):
            all_cells.add(cell)
            for neighbor in automaton.neighbors(cell):
                neighbors_by_cell[neighbor][cell] = cell_type
                all_cells.add(neighbor)

    next_state = defaultdict(lambda: automaton.default_cell_type)

    for cell in all_cells:
        vicinity = MultiStateCellVicinity(
            center_cell=cell,
            center_cell_type=cells.get(cell, automaton.default_cell_type),
            neighbors=neighbors_by_cell[cell],
        )
        new_type = automaton.apply_rule(vicinity)
        if new_type != automaton.default_cell_type:
            next_state[cell] = new_type
    return next_state
