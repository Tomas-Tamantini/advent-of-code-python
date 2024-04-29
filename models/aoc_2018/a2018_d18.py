from enum import Enum
from copy import deepcopy
from typing import Hashable
from models.cellular_automata import (
    Bounded2DAutomaton,
    MultiStateCellVicinity,
    multi_state_automaton_next_state,
)
from models.vectors import Vector2D


class AcreType(str, Enum):
    OPEN = "."
    TREE = "|"
    LUMBERYARD = "#"


class LumberArea(Bounded2DAutomaton):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)

    @property
    def default_cell_type(self) -> AcreType:
        return AcreType.OPEN

    def apply_rule(self, vicinity: MultiStateCellVicinity) -> AcreType:
        if (
            vicinity.center_cell_type == AcreType.OPEN
            and vicinity.num_neighbors_by_type(AcreType.TREE) >= 3
        ):
            return AcreType.TREE
        elif (
            vicinity.center_cell_type == AcreType.TREE
            and vicinity.num_neighbors_by_type(AcreType.LUMBERYARD) >= 3
        ):
            return AcreType.LUMBERYARD
        elif vicinity.center_cell_type == AcreType.LUMBERYARD and (
            not vicinity.has_at_least_one_neighbor_of_type(AcreType.TREE)
            or not vicinity.has_at_least_one_neighbor_of_type(AcreType.LUMBERYARD)
        ):
            return AcreType.OPEN
        return vicinity.center_cell_type

    def _cells_to_hashable(self, cells: dict[Vector2D, AcreType]) -> Hashable:
        return "\n".join(
            "".join(
                cells.get(Vector2D(x, y), AcreType.OPEN) for x in range(self._width)
            )
            for y in range(self._height)
        )

    def next_state(self, cells: dict[Vector2D:Hashable]) -> dict[Vector2D:Hashable]:
        return multi_state_automaton_next_state(self, cells)

    def multi_step(
        self, cells: dict[Vector2D, AcreType], num_steps: int
    ) -> dict[Vector2D, AcreType]:
        current_cells = deepcopy(cells)
        visited: dict[Hashable, int] = dict()
        states: list[tuple[Hashable, dict[Vector2D, AcreType]]] = list()
        for i in range(num_steps):
            current_str = self._cells_to_hashable(current_cells)
            if current_str in visited:
                loop_start = visited[current_str]
                loop_length = i - loop_start
                loop_index = loop_start + (num_steps - loop_start) % loop_length
                return states[loop_index][1]
            visited[current_str] = i
            states.append((current_str, current_cells))
            current_cells = self.next_state(current_cells)
        return current_cells
