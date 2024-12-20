from typing import Iterator

from models.common.graphs import dijkstra

from .amphipod_burrow import AmphipodBurrow


class AmphipodSorter:
    @staticmethod
    def weighted_neighbors(
        burrow: AmphipodBurrow,
    ) -> Iterator[tuple[AmphipodBurrow, int]]:
        yield from burrow.weighted_neighbors()

    def min_energy_to_sort(self, burrow: AmphipodBurrow) -> int:
        origin = burrow
        destination = burrow.terminal_state()
        _, energy = dijkstra(origin, destination, self)
        return energy
