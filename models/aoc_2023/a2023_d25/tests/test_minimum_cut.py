import pytest
from models.common.graphs import UndirectedGraph
from ..minimum_cut import minimum_cut_partition


def test_minimum_cut_of_graph_with_less_than_two_nodes_raises_value_error():
    graph = UndirectedGraph()
    with pytest.raises(ValueError):
        _ = minimum_cut_partition(graph)
    graph.add_node("A")
    with pytest.raises(ValueError):
        _ = minimum_cut_partition(graph)


def test_minimum_cut_of_graph_with_two_nodes_separates_the_two_nodes():
    graph = UndirectedGraph()
    graph.add_edge("a", "b")
    left, right = minimum_cut_partition(graph)
    expected = {frozenset({"a"}), frozenset({"b"})}
    assert expected == {frozenset(left), frozenset(right)}


def test_minimum_cut_partitions_graph_minimizing_edges_between_the_partitions():
    graph = UndirectedGraph()
    graph.add_edge("a", "b")
    graph.add_edge("a", "c")
    graph.add_edge("b", "c")
    graph.add_edge("c", "d")
    left, right = minimum_cut_partition(graph)
    expected = {frozenset({"a", "b", "c"}), frozenset({"d"})}
    assert expected == {frozenset(left), frozenset(right)}


def test_minimum_cut_runs_efficiently():
    graph = UndirectedGraph()
    graph.add_edge("jqt", "rhn")
    graph.add_edge("jqt", "xhk")
    graph.add_edge("jqt", "nvd")
    graph.add_edge("rsh", "frs")
    graph.add_edge("rsh", "pzl")
    graph.add_edge("rsh", "lsr")
    graph.add_edge("xhk", "hfx")
    graph.add_edge("cmg", "qnr")
    graph.add_edge("cmg", "nvd")
    graph.add_edge("cmg", "lhk")
    graph.add_edge("cmg", "bvb")
    graph.add_edge("rhn", "xhk")
    graph.add_edge("rhn", "bvb")
    graph.add_edge("rhn", "hfx")
    graph.add_edge("bvb", "xhk")
    graph.add_edge("bvb", "hfx")
    graph.add_edge("pzl", "lsr")
    graph.add_edge("pzl", "hfx")
    graph.add_edge("pzl", "nvd")
    graph.add_edge("qnr", "nvd")
    graph.add_edge("ntq", "jqt")
    graph.add_edge("ntq", "hfx")
    graph.add_edge("ntq", "bvb")
    graph.add_edge("ntq", "xhk")
    graph.add_edge("nvd", "lhk")
    graph.add_edge("lsr", "lhk")
    graph.add_edge("rzs", "qnr")
    graph.add_edge("rzs", "cmg")
    graph.add_edge("rzs", "lsr")
    graph.add_edge("rzs", "rsh")
    graph.add_edge("frs", "qnr")
    graph.add_edge("frs", "lhk")
    graph.add_edge("frs", "lsr")
    left, right = minimum_cut_partition(graph)
    expected = {
        frozenset({"cmg", "frs", "lhk", "lsr", "nvd", "pzl", "qnr", "rsh", "rzs"}),
        frozenset({"bvb", "hfx", "jqt", "ntq", "rhn", "xhk"}),
    }
    assert expected == {frozenset(left), frozenset(right)}
