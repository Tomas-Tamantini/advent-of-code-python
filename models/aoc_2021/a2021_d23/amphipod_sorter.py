from .amphipod import AmphipodArrangement
from .amphipod_burrow import AmphipodBurrow


class AmphipodSorter:
    def __init__(self, burrow: AmphipodBurrow):
        self._burrow = burrow

    def weight(self, node_a: AmphipodArrangement, node_b: AmphipodArrangement) -> int:
        return node_a.energy_to_move(node_b)

    def min_energy_to_organize(self, initiaL_arrangement: AmphipodArrangement) -> int:
        raise NotImplementedError()
