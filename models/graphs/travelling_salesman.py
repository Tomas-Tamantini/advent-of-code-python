from typing import Hashable
from itertools import permutations


def _total_distance(
    nodes: list[Hashable], distances: dict[tuple[Hashable, Hashable], int]
) -> int:
    total_distance = 0
    for i in range(len(nodes) - 1):
        next_idx = (i + 1) % len(nodes)
        node_a, node_b = nodes[i], nodes[next_idx]
        if (node_a, node_b) in distances:
            dist = distances[(node_a, node_b)]
        else:
            dist = distances[(node_b, node_a)]
        total_distance += dist
    return total_distance


def travelling_salesman(
    initial_node: Hashable,
    distances: dict[tuple[Hashable, Hashable], int],
    must_return_to_origin: bool = True,
) -> int:
    free_nodes = {node for pair in distances.keys() for node in pair}
    free_nodes.discard(initial_node)
    min_dist = float("inf")
    for permutation in permutations(free_nodes):
        nodes = [initial_node] + list(permutation)
        if must_return_to_origin:
            nodes.append(initial_node)
        dist = _total_distance(nodes, distances)
        min_dist = min(min_dist, dist)
    return min_dist
