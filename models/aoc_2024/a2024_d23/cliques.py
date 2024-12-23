from itertools import combinations
from typing import Hashable, Iterator

from models.common.graphs import UndirectedGraph


def three_cliques(graph: UndirectedGraph) -> Iterator[set[Hashable]]:
    for node in graph.nodes():
        neighbors = set(graph.neighbors(node))
        for neighbor_a, neighbor_b in combinations(neighbors, 2):
            if graph.are_connected(neighbor_a, neighbor_b):
                yield frozenset([node, neighbor_a, neighbor_b])


def max_clique(graph: UndirectedGraph) -> set[Hashable]:
    current_cliques = {frozenset([node]) for node in graph.nodes()}
    while True:
        next_cliques = set()
        for clique in current_cliques:
            neighbors = set(graph.neighbors(next(iter(clique))))
            for n in neighbors:
                if all(graph.are_connected(n, c) for c in clique):
                    next_cliques.add(clique | {n})
        if not next_cliques:
            return current_cliques.pop()
        else:
            current_cliques = next_cliques
