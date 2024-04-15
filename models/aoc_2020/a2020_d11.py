from enum import Enum
from models.cellular_automata import MultiState2DAutomaton, CellCluster
from models.vectors import Vector2D


class FerrySeat(str, Enum):
    FLOOR = "."
    EMPTY = "L"
    OCCUPIED = "#"


class FerrySeats(MultiState2DAutomaton):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(
            default_cell_type=FerrySeat.FLOOR,
            width=width,
            height=height,
            consider_diagonal_neighbors=True,
        )

    def apply_rule(self, cluster: CellCluster) -> FerrySeat:
        if (
            cluster.cell_type == FerrySeat.EMPTY
            and cluster.num_neighbors_by_type[FerrySeat.OCCUPIED] == 0
        ):
            return FerrySeat.OCCUPIED
        if (
            cluster.cell_type == FerrySeat.OCCUPIED
            and cluster.num_neighbors_by_type[FerrySeat.OCCUPIED] >= 4
        ):
            return FerrySeat.EMPTY
        return cluster.cell_type

    def steady_state(
        self, state: dict[Vector2D, FerrySeat]
    ) -> dict[Vector2D, FerrySeat]:
        previous_state = None
        current_state = state
        while previous_state != current_state:
            previous_state = current_state
            current_state = self.next_state(current_state)
        return current_state
