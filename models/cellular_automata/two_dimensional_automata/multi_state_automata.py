from collections import defaultdict
from typing import Iterator, Hashable, Optional
from dataclasses import dataclass
from models.vectors import Vector2D


@dataclass(frozen=True)
class CellCluster:
    cell_type: Hashable
    neighbors: list[Hashable]


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

    def _is_within_bounds(self, position: Vector2D) -> bool:
        if self._width is None or self._height is None:
            return True
        return 0 <= position.x < self._width and 0 <= position.y < self._height

    def _neighbors(self, position: Vector2D) -> Iterator[tuple[int, int]]:
        for neighbor in position.adjacent_positions(
            include_diagonals=self._consider_diagonal_neighbors
        ):
            if self._is_within_bounds(neighbor):
                yield neighbor

    def _apply_rule(self, cluster: CellCluster) -> Hashable:
        raise NotImplementedError("Must be implemented by subclass")

    def next_state(self, cells: dict[Vector2D:Hashable]) -> dict[Vector2D:Hashable]:
        all_positions = set()
        neighbors = defaultdict(list)
        for position, cell_type in cells.items():
            if self._is_within_bounds(position):
                all_positions.add(position)
                for neighbor in self._neighbors(position):
                    neighbors[neighbor].append(cell_type)
                    all_positions.add(neighbor)

        next_state = defaultdict(lambda: self._default_cell_type)

        for position in all_positions:
            cluster = CellCluster(
                cell_type=cells.get(position, self._default_cell_type),
                neighbors=tuple(neighbors[position]),
            )
            new_type = self._apply_rule(cluster)
            next_state[position] = new_type
        return next_state
