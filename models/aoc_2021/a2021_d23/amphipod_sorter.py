from typing import Iterator
from models.graphs import dijkstra
from .amphipod_burrow import AmphipodBurrow


class AmphipodSorter:
    def weighted_neighbors(
        self, burrow: AmphipodBurrow
    ) -> Iterator[tuple[AmphipodBurrow, int]]:
        yield from burrow.weighted_neighbors()

    def min_energy_to_sort(self, burrow: AmphipodBurrow) -> int:
        origin = burrow
        destination = burrow.terminal_state()
        _, energy = dijkstra(origin, destination, self)
        return energy
