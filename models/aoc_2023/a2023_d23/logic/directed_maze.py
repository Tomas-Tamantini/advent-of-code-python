from typing import Optional, Iterator
from models.common.graphs import WeightedDirectedGraph
from models.common.vectors import Vector2D, CardinalDirection

# TODO: Refactor this mess, reuse code from maze and grid maze classes


class DirectedMaze(WeightedDirectedGraph):
    def __init__(self) -> None:
        super().__init__()
        self._tile_directions = dict()

    def add_tile(
        self,
        tile: Vector2D,
        tile_direction: Optional[CardinalDirection] = None,
    ) -> None:
        self.add_node(tile)
        if tile_direction:
            self._tile_directions[tile] = tile_direction
        for neighbor in tile.adjacent_positions():
            if neighbor in self._incoming:
                if self._can_connect(tile, neighbor):
                    self.add_edge(tile, neighbor, weight=1)
                if self._can_connect(neighbor, tile):
                    self.add_edge(neighbor, tile, weight=1)

    @staticmethod
    def _connection_direction(tile_a: Vector2D, tile_b: Vector2D) -> CardinalDirection:
        diff = tile_b - tile_a
        return {
            Vector2D(1, 0): CardinalDirection.EAST,
            Vector2D(-1, 0): CardinalDirection.WEST,
            Vector2D(0, 1): CardinalDirection.SOUTH,
            Vector2D(0, -1): CardinalDirection.NORTH,
        }[diff]

    def _can_connect(self, tile_a: Vector2D, tile_b: Vector2D) -> bool:
        connection_direction = self._connection_direction(tile_a, tile_b)
        direction_a = self._tile_directions.get(tile_a)
        direction_b = self._tile_directions.get(tile_b)
        _can_connect_to_a = (direction_a is None) or (
            connection_direction == direction_a
        )
        _can_connect_to_b = (direction_b is None) or (
            connection_direction == direction_b
        )
        return _can_connect_to_a and _can_connect_to_b

    def _nodes_connected_to(self, hub: Vector2D) -> Iterator[Vector2D]:
        yield from self._incoming[hub].keys()
        yield from self._outgoing[hub].keys()

    def _remove_node(self, node: Vector2D) -> None:
        for neighbor in self._incoming[node]:
            del self._outgoing[neighbor][node]
        del self._incoming[node]
        for neighbor in self._outgoing[node]:
            del self._incoming[neighbor][node]
        del self._outgoing[node]

    def _remove_node_and_tie_ends(self, node_with_two_neighbors: Vector2D) -> None:
        a, b = tuple(set(self._nodes_connected_to(node_with_two_neighbors)))
        weight_a_n = self._outgoing[a].get(node_with_two_neighbors)
        weight_n_b = self._outgoing[node_with_two_neighbors].get(b)

        new_weight_ab = (
            weight_a_n + weight_n_b
            if ((weight_a_n is not None) and (weight_n_b is not None))
            else None
        )

        old_weight_ab = self._outgoing[a].get(b)
        if new_weight_ab is not None:
            if (old_weight_ab is None) or (old_weight_ab < new_weight_ab):
                self.add_edge(a, b, new_weight_ab)

        weight_b_n = self._outgoing[b].get(node_with_two_neighbors)
        weight_n_a = self._outgoing[node_with_two_neighbors].get(a)

        new_weight_ba = (
            weight_b_n + weight_n_a
            if ((weight_b_n is not None) and (weight_n_a is not None))
            else None
        )

        old_weight_ba = self._outgoing[b].get(a)
        if new_weight_ba is not None:
            if (old_weight_ba is None) or (old_weight_ba < new_weight_ba):
                self.add_edge(b, a, new_weight_ba)

        self._remove_node(node_with_two_neighbors)

    def _reducible_nodes_with_n_neighbors(
        self, num_neighbors: int, irreducible_nodes: set[Vector2D]
    ) -> Iterator[Vector2D]:
        for node in self._incoming:
            if node not in irreducible_nodes:
                connected_to = set(self._nodes_connected_to(node))
                if len(connected_to) == num_neighbors:
                    yield node

    def reduce(self, irreducible_nodes: set[Vector2D]) -> None:
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
