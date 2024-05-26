from typing import Iterator
from models.common.graphs import Maze
from .valve import Valve


class Volcano:
    def __init__(
        self, valves_graph: Maze, starting_valve: Valve, time_until_eruption: int
    ) -> None:
        self._starting_valve = starting_valve
        self._time_until_eruption = time_until_eruption
        self._graph = valves_graph
        self._reduce_graph()
        self._min_travel_time = min(
            self._graph.weight(a, b)
            for a in self._graph.nodes()
            for b in self._graph.neighbors(a)
        )
        self._min_time_to_open_valve = min(
            v.time_to_open for v in self._graph.nodes() if v.time_to_open > 0
        )

    def _reduce_graph(self) -> None:
        irreducible_nodes = {
            v
            for v in self._graph.nodes()
            if (v.flow_rate > 0 or v == self._starting_valve)
        }
        self._graph.reduce(irreducible_nodes)

    @property
    def starting_valve(self) -> Valve:
        return self._starting_valve

    @property
    def time_until_eruption(self) -> int:
        return self._time_until_eruption

    def all_valves(self) -> Iterator[Valve]:
        yield from self._graph.nodes()

    @property
    def min_travel_time(self) -> int:
        return self._min_travel_time

    @property
    def min_time_to_open_valve(self) -> int:
        return self._min_time_to_open_valve

    def neighboring_valves_with_travel_time(
        self, current_valve: Valve
    ) -> Iterator[tuple[Valve, int]]:
        for neighbor in self._graph.neighbors(current_valve):
            yield neighbor, self._graph.weight(current_valve, neighbor)
