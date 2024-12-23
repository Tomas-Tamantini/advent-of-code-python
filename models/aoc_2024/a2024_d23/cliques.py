from itertools import combinations
from typing import Hashable, Iterator

from models.common.graphs import UndirectedGraph
from models.common.io import ProgressBar


def three_cliques(graph: UndirectedGraph) -> Iterator[set[Hashable]]:
    for node in graph.nodes():
        neighbors = set(graph.neighbors(node))
        for neighbor_a, neighbor_b in combinations(neighbors, 2):
            if graph.are_connected(neighbor_a, neighbor_b):
                yield frozenset([node, neighbor_a, neighbor_b])


def _next_clique_members(
    clique: set[Hashable], graph: UndirectedGraph
) -> Iterator[Hashable]:
    neighbors = set(graph.neighbors(next(iter(clique))))
    for n in neighbors:
        if all(graph.are_connected(n, c) for c in clique):
            yield n


def max_clique(
    graph: UndirectedGraph,
    progress_bar: ProgressBar | None = None,
    expected_max_clique_size: int = -1,
) -> set[Hashable]:
    current_cliques = {frozenset([node]) for node in graph.nodes()}
    while True:
        if progress_bar is not None and expected_max_clique_size > 0:
            clique_size = len(next(iter(current_cliques)))
            progress_bar.update(clique_size, expected_max_clique_size)
        next_cliques = set()
        for clique in current_cliques:
            for n in _next_clique_members(clique, graph):
                next_cliques.add(clique | {n})
        if not next_cliques:
            return current_cliques.pop()
        else:
            current_cliques = next_cliques
