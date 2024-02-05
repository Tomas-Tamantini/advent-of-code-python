from itertools import permutations
from typing import Iterable
from models.graphs import WeightedDirectedGraph


class SeatingArrangements(WeightedDirectedGraph):
    def _round_trip_itinerary_cost(self, itinerary: list[str]):
        return sum(
            self.weight(
                itinerary[i],
                itinerary[(i + 1) % len(itinerary)],
            )
            for i in range(len(itinerary))
        )

    def _round_trips(self) -> Iterable[list[str]]:
        nodes = list(self.nodes())
        for perm in permutations(nodes[1:]):
            yield [nodes[0]] + list(perm)

    def round_trip_itinerary_min_cost(self) -> int:
        return min(
            self._round_trip_itinerary_cost(itinerary)
            for itinerary in self._round_trips()
        )

    def round_trip_itinerary_max_cost(self) -> int:
        return max(
            self._round_trip_itinerary_cost(itinerary)
            for itinerary in self._round_trips()
        )

    def both_ways_trip_max_cost(self) -> int:
        return max(
            self._round_trip_itinerary_cost(itinerary)
            + self._round_trip_itinerary_cost(list(reversed(itinerary)))
            for itinerary in self._round_trips()
        )
