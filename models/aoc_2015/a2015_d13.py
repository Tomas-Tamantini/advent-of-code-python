from itertools import permutations
from typing import Iterable


class DirectedGraph:
    def __init__(self) -> None:
        self._adjacencies: dict[str, dict[str, int]] = dict()

    def add_edge(self, node_a: str, node_b: str, cost: int) -> None:
        if node_a not in self._adjacencies:
            self._adjacencies[node_a] = dict()
        self._adjacencies[node_a][node_b] = cost

    def _cost(self, node_a: str, node_b: str) -> int:
        if node_a not in self._adjacencies:
            return float("inf")
        if node_b not in self._adjacencies[node_a]:
            return float("inf")
        return self._adjacencies[node_a][node_b]

    def _round_trip_itinerary_cost(self, itinerary: Iterable[str]):
        kkk = sum(
            self._cost(
                itinerary[i],
                itinerary[(i + 1) % len(itinerary)],
            )
            for i in range(len(itinerary))
        )

        return sum(
            self._cost(
                itinerary[i],
                itinerary[(i + 1) % len(itinerary)],
            )
            for i in range(len(itinerary))
        )

    def _round_trips(self) -> Iterable[list[str]]:
        nodes = list(self._adjacencies.keys())
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
