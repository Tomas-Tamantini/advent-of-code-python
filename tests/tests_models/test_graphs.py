from models.graphs import min_path_length_with_bfs, explore_with_bfs
import pytest
from dataclasses import dataclass


class MockGraph:
    def is_final_state(self, node):
        return node == "final"

    def neighbors(self, node):
        adjacencies = {
            "a": ("b", "c", "d"),
            "b": ("a", "d"),
            "c": ("final", "b"),
            "d": ("c",),
            "final": tuple(),
            "e": ("f",),
            "f": ("e",),
        }
        return adjacencies[node]


graph = MockGraph()


def test_if_initial_node_is_final_state_then_min_path_is_zero():
    assert min_path_length_with_bfs(graph, initial_node="final") == 0


def test_if_no_path_to_final_state_then_raise_value_error():
    with pytest.raises(ValueError):
        min_path_length_with_bfs(graph, initial_node="f")


def test_minimum_path_from_initial_to_final_node_is_found():
    assert min_path_length_with_bfs(graph, initial_node="a") == 2


def test_can_explore_graph_with_bfs():
    assert list(explore_with_bfs(graph, initial_node="a")) == [
        ("a", 0),
        ("b", 1),
        ("c", 1),
        ("d", 1),
        ("final", 2),
    ]
