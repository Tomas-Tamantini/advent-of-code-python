from enum import Enum
from copy import deepcopy
from typing import Hashable
from models.cellular_automata import MultiState2DAutomaton, CellCluster
from models.vectors import Vector2D


class AcreType(str, Enum):
    OPEN = "."
    TREE = "|"
    LUMBERYARD = "#"


class LumberArea(MultiState2DAutomaton):
    def __init__(self, width: int, height: int) -> None:
        default_cell_type = AcreType.OPEN
        super().__init__(default_cell_type, width, height)

    def _apply_rule(self, cluster: CellCluster) -> AcreType:
        if (
            cluster.cell_type == AcreType.OPEN
            and cluster.neighbors.count(AcreType.TREE) >= 3
        ):
            return AcreType.TREE
        elif (
            cluster.cell_type == AcreType.TREE
            and cluster.neighbors.count(AcreType.LUMBERYARD) >= 3
        ):
            return AcreType.LUMBERYARD
        elif cluster.cell_type == AcreType.LUMBERYARD:
            if (
                AcreType.TREE not in cluster.neighbors
                or AcreType.LUMBERYARD not in cluster.neighbors
            ):
                return AcreType.OPEN
        return cluster.cell_type

    def _cells_to_hashable(self, cells: dict[Vector2D, AcreType]) -> Hashable:
        return "\n".join(
            "".join(
                cells.get(Vector2D(x, y), AcreType.OPEN) for x in range(self._width)
            )
            for y in range(self._height)
        )

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
