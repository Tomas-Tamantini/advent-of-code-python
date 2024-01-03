from itertools import permutations
from typing import Iterable


class AdirectedGraph:
    def __init__(self) -> None:
        self._adjacencies: dict[str, dict[str, int]] = dict()

    def add_edge(self, node_a: str, node_b: str, distance: int) -> None:
        if node_a not in self._adjacencies:
            self._adjacencies[node_a] = dict()
        self._adjacencies[node_a][node_b] = distance

        if node_b not in self._adjacencies:
            self._adjacencies[node_b] = dict()
        self._adjacencies[node_b][node_a] = distance

    @property
    def nodes(self) -> Iterable[str]:
        return self._adjacencies.keys()

    def _distance(self, node_a: str, node_b: str) -> int:
        if node_a not in self._adjacencies:
            return float("inf")
        if node_b not in self._adjacencies[node_a]:
            return float("inf")
        return self._adjacencies[node_a][node_b]

    def _itinerary_distance(self, itinerary: Iterable[str]):
        return sum(
            self._distance(itinerary[i], itinerary[i + 1])
            for i in range(len(itinerary) - 1)
        )

    def shortest_complete_itinerary_distance(self) -> int:
        return min(
            self._itinerary_distance(itinerary)
            for itinerary in permutations(self.nodes)
        )

    def longest_complete_itinerary_distance(self) -> int:
        return max(
            self._itinerary_distance(itinerary)
            for itinerary in permutations(self.nodes)
        )
