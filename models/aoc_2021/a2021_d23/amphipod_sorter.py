from .amphipod import AmphipodArrangement
from .amphipod_burrow import AmphipodBurrow


class AmphipodSorter:
    def __init__(self, burrow: AmphipodBurrow):
        self._burrow = burrow

    def min_energy_to_organize(self, initiaL_arrangement: AmphipodArrangement) -> int:
        raise NotImplementedError()
