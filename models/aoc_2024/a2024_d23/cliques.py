from itertools import combinations
from typing import Hashable, Iterator

from models.common.graphs import UndirectedGraph


def three_cliques(graph: UndirectedGraph) -> Iterator[set[Hashable]]:
    for node in graph.nodes():
        neighbors = set(graph.neighbors(node))
        for neighbor_a, neighbor_b in combinations(neighbors, 2):
            if graph.are_connected(neighbor_a, neighbor_b):
                yield frozenset([node, neighbor_a, neighbor_b])
