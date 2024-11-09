from typing import Hashable
from models.common.graphs import UndirectedGraph


def minimum_cut_partition(
    graph: UndirectedGraph,
) -> tuple[set[Hashable], set[Hashable]]:
    if graph.num_nodes < 2:
        raise ValueError("Graph must have at least 2 nodes")
    nodes = sorted(graph.nodes())
    num_nodes = len(nodes)

    left_group = set(nodes[i] for i in range(0, num_nodes, 2))

    stability_reached = False
    while not stability_reached:
        stability_reached = True
        for node in nodes:
            left_connections = sum(n in left_group for n in graph.neighbors(node))
            right_connections = sum(n not in left_group for n in graph.neighbors(node))
            if (
                (left_connections > right_connections)
                and (node not in left_group)
                and (num_nodes - len(left_group) > 1)
            ):
                left_group.add(node)
                stability_reached = False
            elif (
                (right_connections > left_connections)
                and (node in left_group)
                and (len(left_group) > 1)
            ):
                left_group.remove(node)
                stability_reached = False
    right_group = set(nodes) - left_group
    return left_group, right_group
