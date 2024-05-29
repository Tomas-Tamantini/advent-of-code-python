from itertools import permutations
from models.common.graphs import WeightedUndirectedGraph


class CityRouter(WeightedUndirectedGraph):
    def _itinerary_distance(self, itinerary: tuple[str]) -> int:
        return sum(
            self.weight(itinerary[i], itinerary[i + 1])
            for i in range(len(itinerary) - 1)
        )

    def shortest_complete_itinerary_distance(self) -> int:
        return min(
            self._itinerary_distance(itinerary)
            for itinerary in permutations(self.nodes())
        )

    def longest_complete_itinerary_distance(self) -> int:
        return max(
            self._itinerary_distance(itinerary)
            for itinerary in permutations(self.nodes())
        )
