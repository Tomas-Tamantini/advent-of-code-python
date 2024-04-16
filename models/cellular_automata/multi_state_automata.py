from collections import defaultdict
from typing import Iterator, Hashable, Protocol
from dataclasses import dataclass


Cell = Hashable
CellType = Hashable


@dataclass
class CellCluster:
    cell_type: CellType
    num_neighbors_by_type: dict[CellType:int]


class MultiStateAutomaton(Protocol):
    @property
    def default_cell_type(self) -> CellType: ...

    def is_within_bounds(self, cell: Cell) -> bool: ...

    def neighbors(self, cell: Cell) -> Iterator[Cell]: ...

    def apply_rule(self, cluster: CellCluster) -> CellType: ...


def automaton_next_state(
    automaton: MultiStateAutomaton, cells: dict[Cell:CellType]
) -> dict[Cell:CellType]:
    all_cells = set()
    num_neighbors_by_type = defaultdict(lambda: defaultdict(int))
    for cell, cell_type in cells.items():
        if automaton.is_within_bounds(cell):
            all_cells.add(cell)
            for neighbor in automaton.neighbors(cell):
                num_neighbors_by_type[neighbor][cell_type] += 1
                all_cells.add(neighbor)

    next_state = defaultdict(lambda: automaton.default_cell_type)

    for cell in all_cells:
        cluster = CellCluster(
            cell_type=cells.get(cell, automaton.default_cell_type),
            num_neighbors_by_type=num_neighbors_by_type[cell],
        )
        new_type = automaton.apply_rule(cluster)
        next_state[cell] = new_type
    return next_state
