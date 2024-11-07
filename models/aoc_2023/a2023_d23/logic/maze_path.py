from dataclasses import dataclass
from typing import Hashable
from .maze_edge import MazeEdge


@dataclass(frozen=True)
class MazePath:
    current_node: Hashable
    previously_visited: frozenset[Hashable] = frozenset()
    total_weight: int = 0

    @property
    def num_nodes(self) -> int:
        return len(self.previously_visited) + 1

    def can_add_edge(self, edge: MazeEdge) -> bool:
        return (edge.node_a not in self.previously_visited) and (
            edge.node_b not in self.previously_visited
        )

    def has_visited(self, node: Hashable) -> bool:
        return node in self.previously_visited or node == self.current_node

    def increment(self, new_node: Hashable, weight_increment: int) -> "MazePath":
        return MazePath(
            current_node=new_node,
            previously_visited=self.previously_visited
            | frozenset((self.current_node,)),
            total_weight=self.total_weight + weight_increment,
        )
