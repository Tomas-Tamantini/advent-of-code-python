from enum import Enum
from typing import Iterator, Optional
from models.cellular_automata import CellCluster, automaton_next_state
from models.vectors import Vector2D


class FerrySeat(str, Enum):
    FLOOR = "."
    EMPTY = "L"
    OCCUPIED = "#"


class FerrySeats:
    def __init__(
        self,
        width: int,
        height: int,
        initial_configuration: dict[Vector2D, FerrySeat],
        occupied_neighbors_tolerance: int = 3,
        consider_only_adjacent_neighbors: bool = True,
    ) -> None:
        self._width = width
        self._height = height
        self._occupied_neighbors_tolerance = occupied_neighbors_tolerance
        self._consider_only_adjacent_neighbors = consider_only_adjacent_neighbors
        self._initial_configuration = {
            pos: seat_type
            for pos, seat_type in initial_configuration.items()
            if seat_type != FerrySeat.FLOOR
        }

    @property
    def default_cell_type(self) -> FerrySeat:
        return FerrySeat.FLOOR

    def is_within_bounds(self, cell: Vector2D) -> bool:
        return 0 <= cell.x < self._width and 0 <= cell.y < self._height

    @staticmethod
    def _direction_offset() -> Iterator[Vector2D]:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx == 0 and dy == 0:
                    continue
                yield Vector2D(dx, dy)

    def closest_neighbor(
        self, position: Vector2D, search_direction: Vector2D
    ) -> Optional[Vector2D]:
        step_size = 1
        while True:
            neighbor = position + search_direction * step_size
            if neighbor in self._initial_configuration:
                return neighbor
            elif (
                not self.is_within_bounds(neighbor)
                or self._consider_only_adjacent_neighbors
            ):
                return None
            else:
                step_size += 1

    def neighbors(self, cell: Vector2D) -> Iterator[Vector2D]:
        for offset in self._direction_offset():
            neighbor = self.closest_neighbor(cell, offset)
            if neighbor is not None:
                yield neighbor

    def apply_rule(self, cluster: CellCluster) -> FerrySeat:
        if (
            cluster.cell_type == FerrySeat.EMPTY
            and cluster.num_neighbors_by_type[FerrySeat.OCCUPIED] == 0
        ):
            return FerrySeat.OCCUPIED
        if (
            cluster.cell_type == FerrySeat.OCCUPIED
            and cluster.num_neighbors_by_type[FerrySeat.OCCUPIED]
            > self._occupied_neighbors_tolerance
        ):
            return FerrySeat.EMPTY
        return cluster.cell_type

    def next_state(self, cells: dict[Vector2D:FerrySeat]) -> dict[Vector2D:FerrySeat]:
        return automaton_next_state(self, cells)

    def steady_state(self) -> dict[Vector2D, FerrySeat]:
        previous_state = None
        current_state = self._initial_configuration
        while previous_state != current_state:
            previous_state = current_state
            current_state = self.next_state(current_state)
        return current_state
