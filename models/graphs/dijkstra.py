from .graph import WeightedUndirectedGraph
from heapq import heappop, heappush
from typing import Hashable
from math import inf


def dijkstra(
    origin: Hashable, destination: Hashable, graph: WeightedUndirectedGraph
) -> tuple[list[Hashable], float]:
    distances = {origin: 0}
    previous = {origin: None}
    heap = [(0, origin)]

    while heap:
        current_distance, current_node = heappop(heap)

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
                heappush(heap, (distance, neighbor))

    raise ValueError("No path found")
