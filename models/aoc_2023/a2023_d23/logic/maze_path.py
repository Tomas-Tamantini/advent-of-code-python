from typing import Hashable
from .maze_edge import MazeEdge


# TODO: Check if optimizing this class improves runtime
class MazePath:
    def __init__(self, path: tuple[Hashable], total_weight: int = 0) -> None:
        self._path = path
        self._total_weight = total_weight

    @property
    def total_weight(self) -> int:
        return self._total_weight

    @property
    def current_node(self) -> Hashable:
        return self._path[-1]

    @property
    def num_nodes(self) -> int:
        return len(self._path)

    def can_add_edge(self, edge: MazeEdge) -> bool:
        return edge.node_a not in self._path[:-1] and edge.node_b not in self._path[:-1]

    def __hash__(self) -> int:
        return hash(self._path)

    def __eq__(self, other: "MazePath") -> bool:
        return self._path == other._path

    def has_visited(self, node: Hashable) -> bool:
        return node in self._path

    def increment(self, new_node: Hashable, weight_increment: int) -> "MazePath":
        return MazePath(
            path=self._path + (new_node,),
            total_weight=self._total_weight + weight_increment,
        )
