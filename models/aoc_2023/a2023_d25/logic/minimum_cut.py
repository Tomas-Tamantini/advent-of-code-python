from typing import Hashable
from dataclasses import dataclass
from models.common.graphs import UndirectedGraph
from .stoer_wagner import MergedNodes, build_stoer_wagner_graph


@dataclass(frozen=True)
class _CutOfThePhase:
    merged_nodes: MergedNodes
    weight: int


def minimum_cut_partition(
    graph: UndirectedGraph,
) -> tuple[set[Hashable], set[Hashable]]:
    if graph.num_nodes < 2:
        raise ValueError("Graph must have at least 2 nodes")
    sw_graph = build_stoer_wagner_graph(graph)
    best_cut_of_the_phase = None
    for _ in range(graph.num_nodes - 1):
        print(_, graph.num_nodes)
        sorted_merged_nodes = list(
            sw_graph.maximum_adjacency_sorting(start_node=next(sw_graph.nodes()))
        )
        print("sorted!")
        cut_weight = sw_graph.cut_weight(sorted_merged_nodes[-1])
        if best_cut_of_the_phase is None or cut_weight < best_cut_of_the_phase.weight:
            best_cut_of_the_phase = _CutOfThePhase(
                merged_nodes=sorted_merged_nodes[-1],
                weight=cut_weight,
            )
        sw_graph.merge(sorted_merged_nodes[-1], sorted_merged_nodes[-2])
    left_group = {n for n in best_cut_of_the_phase.merged_nodes.nodes}
    right_group = set(graph.nodes()) - left_group
    return left_group, right_group
