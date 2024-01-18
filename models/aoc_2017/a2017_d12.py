from collections import defaultdict
from typing import Hashable


class ProgramGraph:
    def __init__(self):
        self._adjacencies = defaultdict(set)

    @property
    def num_nodes(self) -> int:
        return len(self._adjacencies)

    def add_edge(self, node_a: Hashable, node_b: Hashable) -> None:
        if node_a == node_b:
            self._adjacencies[node_a] = set()
        else:
            self._adjacencies[node_a].add(node_b)
            self._adjacencies[node_b].add(node_a)

    def neighbors(self, node: Hashable) -> set[Hashable]:
        return self._adjacencies[node]
