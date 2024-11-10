from typing import Hashable, Iterator, Iterable
from collections import defaultdict
from dataclasses import dataclass
from models.common.graphs import WeightedUndirectedGraph, UndirectedGraph


@dataclass(frozen=True)
class MergedNodes:
    nodes: tuple[Hashable, ...]

    def merge(self, other: "MergedNodes") -> "MergedNodes":
        return MergedNodes(self.nodes + other.nodes)


class StoerWagnerGraph(WeightedUndirectedGraph):
    def _weight_between_node_and_group(
        self, node: MergedNodes, group: Iterable[MergedNodes]
    ) -> int:
        return sum(
            self.weight(grouped_node, node)
            for grouped_node in group
            if self.has_edge(grouped_node, node)
        )

    def merge(self, node_a: MergedNodes, node_b: MergedNodes) -> None:
        new_node = node_a.merge(node_b)
        self.add_node(new_node)
        new_weights = defaultdict(int)
        for neighbor in self.neighbors(node_a):
            new_weights[neighbor] += self.weight(node_a, neighbor)
        for neighbor in self.neighbors(node_b):
            new_weights[neighbor] += self.weight(node_b, neighbor)
        for neighbor, weight in new_weights.items():
            self.add_edge(new_node, neighbor, weight)
        self.remove_node(node_a)
        self.remove_node(node_b)

    def cut_weight(self, node: MergedNodes) -> int:
        return sum(self.weight(node, neighbor) for neighbor in self.neighbors(node))

    def maximum_adjacency_sorting(
        self, start_node: MergedNodes
    ) -> Iterator[MergedNodes]:
        grouped = set()
        queued = {start_node}
        while queued:
            if len(queued) == 1:
                next_node = queued.pop()
            else:
                next_node = max(
                    queued,
                    key=lambda n: self._weight_between_node_and_group(n, grouped),
                )
                queued.remove(next_node)
            yield next_node
            grouped.add(next_node)
            for n in self.neighbors(next_node):
                if n not in grouped:
                    queued.add(n)


def build_stoer_wagner_graph(graph: UndirectedGraph) -> StoerWagnerGraph:
    sw_graph = StoerWagnerGraph()
    for node in graph.nodes():
        for neighbor in graph.neighbors(node):
            sw_graph.add_edge(MergedNodes((node,)), MergedNodes((neighbor,)), weight=1)
    return sw_graph
