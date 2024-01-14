from typing import Iterator, Hashable
from .graph import Graph


def min_path_length_with_bfs(graph: Graph, initial_node: Hashable) -> int:
    if graph.is_final_state(initial_node):
        return 0
    queue = [(initial_node, 0)]
    visited = {initial_node}
    while queue:
        node, distance = queue.pop(0)
        for neighbor in graph.neighbors(node):
            if graph.is_final_state(neighbor):
                return distance + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    raise ValueError("No path to final state found")


def explore_with_bfs(
    graph: Graph, initial_node: Hashable
) -> Iterator[tuple[Hashable, int]]:
    queue = [(initial_node, 0)]
    visited = {initial_node}
    while queue:
        node, distance = queue.pop(0)
        yield node, distance
        for neighbor in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
