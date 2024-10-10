from typing import Hashable, Protocol, Callable
from math import inf
from dataclasses import dataclass, field
from queue import PriorityQueue
from .dijkstra import WeightedGraph
from dataclasses import dataclass


class AStarGraphProtocol(WeightedGraph, Protocol):
    def heuristic_potential(self, node: Hashable) -> float: ...


@dataclass(frozen=True, order=True)
class _PriorityItem:
    priority: float
    actual_distance: float
    item: Hashable = field(compare=False)


def a_star(
    origin: Hashable,
    is_destination: Callable[[Hashable], bool],
    graph: AStarGraphProtocol,
) -> tuple[list[Hashable], float]:
    distances = {origin: 0}
    previous = {origin: None}
    queue = PriorityQueue()
    queue.put(_PriorityItem(0, 0, origin))

    while not queue.empty():
        current = queue.get()
        current_node = current.item
        current_distance = current.actual_distance

        if is_destination(current_node):
            path = []
            while current_node:
                path.append(current_node)
                current_node = previous[current_node]
            return path[::-1], current_distance

        for neighbor in graph.neighbors(current_node):
            distance = current_distance + graph.weight(current_node, neighbor)
            if distance < distances.get(neighbor, inf):
                distances[neighbor] = distance
                previous[neighbor] = current_node
                queue.put(
                    _PriorityItem(
                        distance + graph.heuristic_potential(neighbor),
                        distance,
                        neighbor,
                    )
                )

    raise ValueError("No path found")
