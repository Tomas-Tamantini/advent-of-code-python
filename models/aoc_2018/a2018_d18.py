from enum import Enum
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
