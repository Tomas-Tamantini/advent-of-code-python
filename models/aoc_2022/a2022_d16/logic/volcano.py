from typing import Iterator
from models.common.graphs import Maze
from .valve import Valve


class Volcano:
    def __init__(self, valves_graph: Maze, starting_valve: Valve) -> None:
        self._graph = valves_graph
        irreducible_nodes = {
            v for v in valves_graph.nodes() if (v.flow_rate > 0 or v == starting_valve)
        }
        self._graph.reduce(irreducible_nodes)
        self._min_travel_time = min(
            self._graph.weight(a, b)
            for a in self._graph.nodes()
            for b in self._graph.neighbors(a)
        )

    def all_valves(self) -> Iterator[Valve]:
        yield from self._graph.nodes()

    @property
    def min_travel_time(self) -> int:
        return self._min_travel_time

    def neighboring_valves_with_travel_time(
        self, current_valve: Valve
    ) -> Iterator[tuple[Valve, int]]:
        for neighbor in self._graph.neighbors(current_valve):
            yield neighbor, self._graph.weight(current_valve, neighbor)
