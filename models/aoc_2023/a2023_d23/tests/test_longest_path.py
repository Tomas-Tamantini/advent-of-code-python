import pytest
from math import inf
from models.common.graphs import WeightedDirectedGraph
from ..logic import max_length_non_repeating_path


def test_max_length_non_repeating_path_is_zero_if_start_equals_end():
    graph = WeightedDirectedGraph()
    graph.add_node("A")
    assert 0 == max_length_non_repeating_path(graph, "A", "A")


def test_max_length_non_repeating_path_is_minus_inf_if_no_path():
    graph = WeightedDirectedGraph()
    graph.add_node("A")
    graph.add_node("B")
    graph.add_edge("B", "A", 123)
    assert -inf == max_length_non_repeating_path(graph, "A", "B")


def test_max_length_non_repeating_path_is_path_length_if_one_possible_path():
    graph = WeightedDirectedGraph()
    graph.add_node("A")
    graph.add_node("B")
    graph.add_edge("A", "B", 123)
    assert 123 == max_length_non_repeating_path(graph, "A", "B")


def test_max_length_non_repeating_path_is_path_with_maximum_weight():
    graph = WeightedDirectedGraph()
    graph.add_node("A")
    graph.add_node("B")
    graph.add_node("C")
    graph.add_edge("A", "B", 1)
    graph.add_edge("A", "C", 2)
    graph.add_edge("C", "B", 3)
    assert 5 == max_length_non_repeating_path(graph, "A", "B")


def test_max_length_non_repeating_path_does_not_visit_same_node_more_than_once():
    graph = WeightedDirectedGraph()
    for node in "ABCDE":
        graph.add_node(node)
    graph.add_edge("A", "B", 1)
    graph.add_edge("B", "C", 1)
    graph.add_edge("C", "D", 1)
    graph.add_edge("D", "B", 1)
    graph.add_edge("B", "E", 1)
    assert 2 == max_length_non_repeating_path(graph, "A", "E")


@pytest.mark.skip("Test takes about 2s to run")
def test_max_length_non_repeating_path_runs_efficiently():
    graph = WeightedDirectedGraph()
    size = 6
    for row in range(size):
        for col in range(size):
            node = (row, col)
            graph.add_node(node)
            if row > 0:
                node_top = (row - 1, col)
                weight = 1 + size * row + col
                graph.add_edge(node, node_top, weight)
                graph.add_edge(node_top, node, weight)
            if col > 0:
                node_left = (row, col - 1)
                weight = size * (1 + size * row + col)
                graph.add_edge(node, node_left, weight)
                graph.add_edge(node_left, node, weight)
    start = (0, 0)
    end = (size - 1, size - 1)
    assert 3405 == max_length_non_repeating_path(graph, start, end)
