from collections import defaultdict
from typing import Iterator, Hashable, Optional, Protocol
from dataclasses import dataclass
from models.vectors import Vector2D


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


class MultiState2DAutomaton:
    def __init__(
        self,
        default_cell_type: Hashable = 0,
        width: Optional[int] = None,
        height: Optional[int] = None,
        consider_diagonal_neighbors: bool = True,
    ) -> None:
        self._default_cell_type = default_cell_type
        self._width = width
        self._height = height
        self._consider_diagonal_neighbors = consider_diagonal_neighbors

    @property
    def default_cell_type(self) -> Hashable:
        return self._default_cell_type

    @property
    def width(self) -> Optional[int]:
        return self._width

    @property
    def height(self) -> Optional[int]:
        return self._height

    def is_within_bounds(self, cell: Vector2D) -> bool:
        if self._width is None or self._height is None:
            return True
        return 0 <= cell.x < self._width and 0 <= cell.y < self._height

    def neighbors(self, cell: Vector2D) -> Iterator[Cell]:
        for neighbor in cell.adjacent_positions(
            include_diagonals=self._consider_diagonal_neighbors
        ):
            if self.is_within_bounds(neighbor):
                yield neighbor

    def apply_rule(self, cluster: CellCluster) -> CellType:
        raise NotImplementedError("Must be implemented by subclass")

    def next_state(self, cells: dict[Vector2D:Hashable]) -> dict[Vector2D:Hashable]:
        return automaton_next_state(self, cells)
