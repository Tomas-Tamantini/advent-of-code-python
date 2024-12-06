from collections import deque
from dataclasses import dataclass
from typing import Hashable, Optional

from models.common.graphs import UndirectedGraph
from models.common.io import ProgressBar

from .stoer_wagner import MergedNodes, build_stoer_wagner_graph


@dataclass(frozen=True)
class _CutOfThePhase:
    merged_nodes: MergedNodes
    weight: int

    def partition(
        self, all_nodes: set[Hashable]
    ) -> tuple[set[Hashable], set[Hashable]]:
        left_group = {n for n in self.merged_nodes.nodes}
        right_group = all_nodes - left_group
        return left_group, right_group


def minimum_cut_partition(
    graph: UndirectedGraph,
    minimum_cut_lower_bound: int = 0,
    progress_bar: Optional[ProgressBar] = None,
) -> tuple[set[Hashable], set[Hashable]]:
    num_nodes = graph.num_nodes
    if num_nodes < 2:
        raise ValueError("Graph must have at least 2 nodes")
    sw_graph = build_stoer_wagner_graph(graph)
    best_cut_of_the_phase = None
    for i in range(num_nodes - 1):
        if progress_bar:
            progress_bar.update(i, num_nodes)
        penultimate_node, last_node = deque(
            sw_graph.maximum_adjacency_sorting(start_node=next(sw_graph.nodes())),
            maxlen=2,
        )
        cut_weight = sw_graph.cut_weight(last_node)
        if best_cut_of_the_phase is None or cut_weight < best_cut_of_the_phase.weight:
            best_cut_of_the_phase = _CutOfThePhase(
                merged_nodes=last_node, weight=cut_weight
            )
            if cut_weight <= minimum_cut_lower_bound:
                break
        sw_graph.merge(penultimate_node, last_node)
    return best_cut_of_the_phase.partition(all_nodes=set(graph.nodes()))
