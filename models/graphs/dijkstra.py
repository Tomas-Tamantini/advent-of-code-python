from .graph import GraphProtocol, WeightedProtocol
from typing import Hashable, Protocol
from math import inf
from dataclasses import dataclass, field
from queue import PriorityQueue


class _WeightedGraph(GraphProtocol, WeightedProtocol, Protocol):
    pass


@dataclass(frozen=True, order=True)
class _PriorityItem:
    priority: float
    item: Hashable = field(compare=False)


def dijkstra(
    origin: Hashable,
    destination: Hashable,
    graph: _WeightedGraph,
) -> tuple[list[Hashable], float]:
    distances = {origin: 0}
    previous = {origin: None}
    queue = PriorityQueue()
    queue.put(_PriorityItem(0, origin))

    while not queue.empty():
        current = queue.get()
        current_node = current.item
        current_distance = current.priority

        if current_node == destination:
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
                queue.put(_PriorityItem(distance, neighbor))

    raise ValueError("No path found")
