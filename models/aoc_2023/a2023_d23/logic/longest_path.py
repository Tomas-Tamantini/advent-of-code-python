from typing import Hashable
from models.common.graphs import WeightedDirectedGraph
from models.common.optimization.branch_and_bound import maximize_with_branch_and_bound
from .maze_path import MazePath
from .maze_explorer import MazeExplorer


def max_length_non_repeating_path(
    graph: WeightedDirectedGraph, start_node: Hashable, end_node: Hashable
) -> int:
    length = 0
    destination_neighbors = list(graph.incoming(end_node))
    if len(destination_neighbors) == 1:
        destination_neighbor = destination_neighbors[0]
        length = graph.weight(destination_neighbor, end_node)
        end_node = destination_neighbor
    return length + maximize_with_branch_and_bound(
        initial_state=MazePath(path=(start_node,)),
        state_explorer=MazeExplorer(graph, end_node),
    )
