from math import inf
from typing import Iterator, Hashable
from models.common.graphs import WeightedDirectedGraph
from .maze_path import MazePath
from .maze_edge import MazeEdge


class MazeExplorer:
    def __init__(self, graph: WeightedDirectedGraph, end_node: Hashable) -> None:
        self._graph = graph
        self._end_node = end_node
        self._edges = sorted(list(self._build_edges()), key=lambda e: -e.weight)

    def _build_edges(self) -> Iterator[MazeEdge]:
        weights = dict()
        for node in self._graph.nodes():
            for neighbor in self._graph.neighbors(node):
                pair = frozenset((node, neighbor))
                weight = self._graph.weight(node, neighbor)
                weight = max(weight, weights.get(pair, 0))
                weights[pair] = weight
        for pair, weight in weights.items():
            yield MazeEdge(*tuple(pair), weight)

    def _path_is_terminal(self, path: MazePath) -> bool:
        return path.current_node == self._end_node

    def objective_value(self, state: MazePath) -> float:
        return state.total_weight if self._path_is_terminal(state) else -inf

    def _remaining_edges(self, path: MazePath) -> Iterator[MazeEdge]:
        num_remaining_nodes = self._graph.num_nodes - path.num_nodes
        edge_count = 0
        for edge in self._edges:
            if path.can_add_edge(edge):
                yield edge
                edge_count += 1
                if edge_count >= num_remaining_nodes:
                    break

    def upper_bound_on_objective_value(self, state: MazePath) -> float:
        if self._path_is_terminal(state):
            return state.total_weight
        return state.total_weight + sum(
            edge.weight for edge in self._remaining_edges(state)
        )

    def children_states(self, state: MazePath) -> Iterator[MazePath]:
        if not self._path_is_terminal(state):
            for neighbor in self._graph.neighbors(state.current_node):
                if not state.has_visited(neighbor):
                    weight = self._graph.weight(state.current_node, neighbor)
                    yield state.increment(new_node=neighbor, weight_increment=weight)
