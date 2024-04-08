from typing import Iterator
from math import inf
from models.vectors import Vector2D


class TunnelMazeGraph:

    def __init__(self) -> None:
        self._adjacencies = dict()

    @property
    def num_nodes(self) -> int:
        return len(self._adjacencies)

    def add_node(self, node: Vector2D) -> None:
        if node not in self._adjacencies:
            self._adjacencies[node] = dict()
        for neighbor in node.adjacent_positions(include_diagonals=False):
            if neighbor not in self._adjacencies:
                continue
            self._adjacencies[node][neighbor] = 1
            self._adjacencies[neighbor][node] = 1

    def weight(self, node_a: Vector2D, node_b: Vector2D) -> float:
        return self._adjacencies[node_a].get(node_b, inf)

    def _remove_node(self, node: Vector2D) -> None:
        for neighbor in self._adjacencies[node]:
            del self._adjacencies[neighbor][node]
        del self._adjacencies[node]

    def _remove_node_and_tie_ends(self, node_with_two_neighbors: Vector2D) -> None:
        neighbor_a, neighbor_b = self._adjacencies[node_with_two_neighbors].keys()
        weight_a = self.weight(node_with_two_neighbors, neighbor_a)
        weight_b = self.weight(node_with_two_neighbors, neighbor_b)
        new_weight = weight_a + weight_b
        self._remove_node(node_with_two_neighbors)
        self._try_add_edge(neighbor_a, neighbor_b, new_weight)

    def _try_add_edge(self, node_a: Vector2D, node_b: Vector2D, weight: float) -> None:
        previous_weight = self.weight(node_a, node_b)
        new_weight = min(previous_weight, weight)
        self._adjacencies[node_a][node_b] = new_weight
        self._adjacencies[node_b][node_a] = new_weight

    def _reducible_nodes_with_n_neighbors(
        self, num_neighbors: int, irreducible_nodes: set[Vector2D]
    ) -> Iterator[Vector2D]:
        for node, neighbors in self._adjacencies.items():
            if node not in irreducible_nodes and len(neighbors) == num_neighbors:
                yield node

    def reduce(self, irreducible_nodes: set[Vector2D]) -> None:
        next_one_neighbor = next(
            self._reducible_nodes_with_n_neighbors(1, irreducible_nodes), None
        )
        if next_one_neighbor is not None:
            self._remove_node(next_one_neighbor)
            self.reduce(irreducible_nodes)
        else:
            next_two_neighbors = next(
                self._reducible_nodes_with_n_neighbors(2, irreducible_nodes), None
            )
            if next_two_neighbors is not None:
                self._remove_node_and_tie_ends(next_two_neighbors)
                self.reduce(irreducible_nodes)
