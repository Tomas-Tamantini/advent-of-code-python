from typing import Hashable, Protocol, Iterator, Union, runtime_checkable
from math import inf
from dataclasses import dataclass, field
from queue import PriorityQueue
from .graph import GraphProtocol, WeightedProtocol


class WeightedGraph(GraphProtocol, WeightedProtocol, Protocol):
    pass


@runtime_checkable
class SingleMethodWeightedGraph(Protocol):
    def weighted_neighbors(self, node: Hashable) -> Iterator[tuple[Hashable, int]]: ...


@dataclass(frozen=True, order=True)
class _PriorityItem:
    priority: float
    item: Hashable = field(compare=False)


def _weighted_neighbors(
    node: Hashable, graph: Union[WeightedGraph, SingleMethodWeightedGraph]
) -> Iterator[tuple[Hashable, int]]:
    if isinstance(graph, SingleMethodWeightedGraph):
        yield from graph.weighted_neighbors(node)
    else:
        for neighbor in graph.neighbors(node):
            yield neighbor, graph.weight(node, neighbor)


def dijkstra(
    origin: Hashable,
    destination: Hashable,
    graph: Union[WeightedGraph, SingleMethodWeightedGraph],
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

        for neighbor, weight in _weighted_neighbors(current_node, graph):
            distance = current_distance + weight
            if distance < distances.get(neighbor, inf):
                distances[neighbor] = distance
                previous[neighbor] = current_node
                queue.put(_PriorityItem(distance, neighbor))

    raise ValueError("No path found")
