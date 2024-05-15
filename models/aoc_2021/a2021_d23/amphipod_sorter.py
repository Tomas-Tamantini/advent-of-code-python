from .amphipod import AmphipodArrangement
from .amphipod_burrow import AmphipodBurrow


class AmphipodSorter:
    def __init__(self, burrow: AmphipodBurrow):
        self._burrow = burrow

    def weight(self, node_a: AmphipodArrangement, node_b: AmphipodArrangement) -> int:
        return sum(
            amph_a.energy_to_move(amph_b.position)
            for amph_a, amph_b in zip(node_a.amphipods, node_b.amphipods)
        )

    def min_energy_to_organize(self, initiaL_arrangement: AmphipodArrangement) -> int:
        raise NotImplementedError()
