from models.common.graphs import UndirectedGraph
from ..logic import build_stoer_wagner_graph, MergedNodes, StoerWagnerGraph


def test_stoer_wagner_graph_starts_with_no_merged_nodes():
    graph = UndirectedGraph()
    graph.add_edge("a", "b")
    sw_graph = build_stoer_wagner_graph(graph)
    assert set(sw_graph.nodes()) == {MergedNodes(("a",)), MergedNodes(("b",))}


def test_stoer_wagner_graph_starts_with_weight_one_for_all_edges():
    graph = UndirectedGraph()
    graph.add_edge("a", "b")
    sw_graph = build_stoer_wagner_graph(graph)
    assert sw_graph.weight(MergedNodes(("a",)), MergedNodes(("b",))) == 1


def test_stoer_wagner_graph_sorts_nodes_by_maximum_adjacency():
    # Example taken from article: A Simple Min-Cut Algorithm
    nodes = {
        "a": MergedNodes((2,)),
        "b": MergedNodes((3,)),
        "c": MergedNodes((4,)),
        "d": MergedNodes((7,)),
        "e": MergedNodes((8,)),
        "f": MergedNodes((6,)),
        "s": MergedNodes((5,)),
        "t": MergedNodes((1,)),
    }
    edges = [
        ("t", "a", 2),
        ("a", "b", 3),
        ("b", "c", 4),
        ("s", "f", 3),
        ("f", "d", 1),
        ("d", "e", 3),
        ("t", "s", 3),
        ("a", "f", 2),
        ("b", "d", 2),
        ("c", "e", 2),
        ("s", "a", 2),
        ("d", "c", 2),
    ]
    sw_graph = StoerWagnerGraph()
    for n_a, n_b, weight in edges:
        sw_graph.add_edge(nodes[n_a], nodes[n_b], weight)

    sorted_nodes = list(sw_graph.maximum_adjacency_sorting(start_node=nodes["a"]))
    expected = [nodes[x] for x in "abcdefst"]
    assert expected == sorted_nodes


def test_stoer_wagner_cut_weight_is_sum_of_weight_of_all_edges_from_node():
    node_a = MergedNodes((1, 5))
    node_b = MergedNodes((2,))
    node_c = MergedNodes((3, 4, 6))
    sw_graph = StoerWagnerGraph()
    sw_graph.add_edge(node_a, node_b, 10)
    sw_graph.add_edge(node_a, node_c, 5)
    sw_graph.add_edge(node_b, node_c, 3)
    assert sw_graph.cut_weight(node_a) == 15
    assert sw_graph.cut_weight(node_b) == 13
    assert sw_graph.cut_weight(node_c) == 8


def test_merging_stoer_wagner_nodes_removes_old_nodes_and_adds_new_one_with_added_adges():
    node_a = MergedNodes((1, 5))
    node_b = MergedNodes((2,))
    node_c = MergedNodes((3, 4, 6))
    sw_graph = StoerWagnerGraph()
    sw_graph.add_edge(node_a, node_b, 10)
    sw_graph.add_edge(node_a, node_c, 5)
    sw_graph.add_edge(node_b, node_c, 3)
    sw_graph.merge(node_a, node_b)
    assert sw_graph.num_nodes == 2
    merged = next(sw_graph.neighbors(node_c))
    assert merged == MergedNodes((1, 5, 2))
    assert sw_graph.weight(node_c, merged) == 8
