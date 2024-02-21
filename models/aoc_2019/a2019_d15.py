from typing import Iterator, Optional
from enum import Enum
from models.vectors import Vector2D, CardinalDirection
from models.graphs import min_path_length_with_bfs, explore_with_bfs
from .intcode import IntcodeProgram, run_intcode_program


class CellType(Enum):
    EMPTY = 0
    WALL = 1
    OXYGEN_SYSTEM = 2


class DroidExploredArea:
    def __init__(self) -> None:
        self._cells = dict()
        self._oxygen_system = None

    @property
    def position_oxygen_system(self) -> Vector2D:
        return self._oxygen_system

    @property
    def explored_cells(self) -> set[Vector2D]:
        return set(self._cells.keys())

    @property
    def empty_cells(self) -> set[Vector2D]:
        return {
            cell
            for cell, cell_type in self._cells.items()
            if cell_type in (CellType.EMPTY, CellType.OXYGEN_SYSTEM)
        }

    def set_cell(self, cell: Vector2D, cell_type: CellType) -> None:
        self._cells[cell] = cell_type
        if cell_type == CellType.OXYGEN_SYSTEM:
            self._oxygen_system = cell

    def neighbors(self, node: Vector2D) -> Iterator[Vector2D]:
        for neighbor in node.adjacent_positions():
            if self._cells.get(neighbor, CellType.WALL) != CellType.WALL:
                yield neighbor

    def distance_to_oxygen_system(self, starting_point: Vector2D) -> int:
        return min_path_length_with_bfs(
            graph=self,
            initial_node=starting_point,
            is_final_state=lambda node: node == self._oxygen_system,
        )

    def minutes_to_fill_with_oxygen(self) -> int:
        for _, distance in explore_with_bfs(
            graph=self, initial_node=self._oxygen_system
        ):
            minutes = distance
        return minutes


class RepairDroid:
    def __init__(self, initial_position: Vector2D = Vector2D(0, 0)) -> None:
        self._position = initial_position
        self._directions = []

    @property
    def position(self) -> Vector2D:
        return self._position

    def move(self, direction: CardinalDirection) -> None:
        self._position = self._position.move(direction)
        if direction == self.backtrack_direction():
            self._directions.pop()
        else:
            self._directions.append(direction)

    def backtrack_direction(self) -> Optional[CardinalDirection]:
        if self._directions:
            return self._directions[-1].reverse()


class RepairDroidIO:
    def __init__(self, droid: RepairDroid, area: DroidExploredArea) -> None:
        self._area = area
        self._droid = droid
        self._area.set_cell(self._droid.position, CellType.EMPTY)
        self._last_attempted_direction = None

    def write(self, value: int) -> None:
        if value == 0:
            self._area.set_cell(
                self._droid.position.move(self._last_attempted_direction), CellType.WALL
            )
        elif value == 1:
            self._droid.move(self._last_attempted_direction)
            self._area.set_cell(self._droid.position, CellType.EMPTY)
        elif value == 2:
            self._droid.move(self._last_attempted_direction)
            self._area.set_cell(self._droid.position, CellType.OXYGEN_SYSTEM)

    def _possible_directions(self) -> Iterator[CardinalDirection]:
        for direction in CardinalDirection:
            if self._droid.position.move(direction) not in self._area.explored_cells:
                yield direction

    def _next_direction(self) -> CardinalDirection:
        for direction in self._possible_directions():
            return direction
        return self._droid.backtrack_direction()

    def read(self) -> int:
        direction = self._next_direction()
        if direction is None:
            raise StopIteration("No more directions to explore")
        self._last_attempted_direction = direction
        return {
            CardinalDirection.NORTH: 1,
            CardinalDirection.SOUTH: 2,
            CardinalDirection.WEST: 3,
            CardinalDirection.EAST: 4,
        }[direction]


def repair_droid_explore_area(
    area: DroidExploredArea, droid_instructions: list[int]
) -> None:
    program = IntcodeProgram(droid_instructions[:])
    droid = RepairDroid()
    io = RepairDroidIO(droid, area)
    run_intcode_program(program, serial_input=io, serial_output=io)
