from typing import Iterator, Hashable
from math import inf
from models.common.vectors import Vector2D
from .dijkstra import dijkstra
from .graph import WeightedUndirectedGraph


class Maze(WeightedUndirectedGraph):
    def _remove_node(self, node: Hashable) -> None:
        for neighbor in self._adjacencies[node]:
            del self._adjacencies[neighbor][node]
        del self._adjacencies[node]

    def _remove_node_and_tie_ends(self, node_with_two_neighbors: Hashable) -> None:
        neighbor_a, neighbor_b = self._adjacencies[node_with_two_neighbors].keys()
        weight_a = self.weight(node_with_two_neighbors, neighbor_a)
        weight_b = self.weight(node_with_two_neighbors, neighbor_b)
        new_weight = weight_a + weight_b
        self._remove_node(node_with_two_neighbors)
        self._try_add_edge(neighbor_a, neighbor_b, new_weight)

    def _try_add_edge(self, node_a: Hashable, node_b: Hashable, weight: float) -> None:
        previous_weight = self.weight(node_a, node_b)
        new_weight = min(previous_weight, weight)
        self._adjacencies[node_a][node_b] = new_weight
        self._adjacencies[node_b][node_a] = new_weight

    def _reducible_nodes_with_n_neighbors(
        self, num_neighbors: int, irreducible_nodes: set[Hashable]
    ) -> Iterator[Hashable]:
        for node, neighbors in self._adjacencies.items():
            if node not in irreducible_nodes and len(neighbors) == num_neighbors:
                yield node

    def reduce(self, irreducible_nodes: set[Hashable]) -> None:
        graph_changed = False
        one_neighbors = list(
            self._reducible_nodes_with_n_neighbors(1, irreducible_nodes)
        )
        for node in one_neighbors:
            graph_changed = True
            self._remove_node(node)
        two_neighbors = list(
            self._reducible_nodes_with_n_neighbors(2, irreducible_nodes)
        )
        for node in two_neighbors:
            graph_changed = True
            self._remove_node_and_tie_ends(node)
        if graph_changed:
            self.reduce(irreducible_nodes)

    def shortest_distance(self, origin: Hashable, destination: Hashable) -> float:
        try:
            return dijkstra(origin, destination, self)[1]
        except ValueError:
            return inf


class GridMaze(Maze):
    def add_node_and_connect_to_neighbors(self, node: Vector2D) -> None:
        if node not in self._adjacencies:
            self._adjacencies[node] = dict()
        for neighbor in node.adjacent_positions(include_diagonals=False):
            if neighbor not in self._adjacencies:
                continue
            self._adjacencies[node][neighbor] = 1
            self._adjacencies[neighbor][node] = 1
