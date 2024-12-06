from collections import defaultdict
from typing import Hashable, Iterator

from models.common.graphs import explore_with_bfs


class ProgramGraph:
    def __init__(self):
        self._adjacencies = defaultdict(set)

    @property
    def num_nodes(self) -> int:
        return len(self._adjacencies)

    def add_edge(self, node_a: Hashable, node_b: Hashable) -> None:
        self._adjacencies[node_a].add(node_b)
        self._adjacencies[node_b].add(node_a)

    def neighbors(self, node: Hashable) -> set[Hashable]:
        return self._adjacencies[node]

    def disjoint_groups(self) -> Iterator[set[Hashable]]:
        visited = set()
        for node in self._adjacencies:
            if node in visited:
                continue
            group = set(n for n, _ in explore_with_bfs(self, node))
            visited |= group
            yield group
