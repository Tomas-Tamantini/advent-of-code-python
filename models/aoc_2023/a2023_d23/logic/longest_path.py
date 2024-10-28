from typing import Hashable
from math import inf
from models.common.graphs import WeightedDirectedGraph


def max_length_non_repeating_path(
    graph: WeightedDirectedGraph, start_node: Hashable, end_node: Hashable
) -> int:
    visited = set()
    current_node = start_node
    return _max_length_recursive(graph, current_node, end_node, visited)


def _max_length_recursive(
    graph: WeightedDirectedGraph,
    current_node: Hashable,
    end_node: Hashable,
    visited: set[Hashable],
) -> int:
    if current_node == end_node:
        return 0
    if current_node in visited:
        return -inf
    max_length = -1
    visited.add(current_node)
    for neighbor in graph.neighbors(current_node):
        new_length = graph.weight(current_node, neighbor) + _max_length_recursive(
            graph, neighbor, end_node, visited
        )
        max_length = max(max_length, new_length)
    visited.remove(current_node)
    return max_length
