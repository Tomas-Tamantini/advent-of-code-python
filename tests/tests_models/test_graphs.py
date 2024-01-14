from models.graphs import (
    min_path_length_with_bfs,
    explore_with_bfs,
    travelling_salesman,
)
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


def test_travelling_salesman_of_single_city_is_zero():
    assert travelling_salesman(initial_node="0", distances={}) == 0


distances = {
    ("0", "1"): 2,
    ("0", "2"): 8,
    ("0", "3"): 10,
    ("0", "4"): 2,
    ("1", "2"): 6,
    ("1", "3"): 8,
    ("1", "4"): 4,
    ("2", "3"): 2,
    ("2", "4"): 10,
    ("3", "4"): 8,
}


def test_travelling_salesman_must_make_round_trip_by_default():
    assert travelling_salesman(initial_node="0", distances=distances) == 20


def test_travelling_salesman_can_end_trip_before_returning_to_origin():
    assert (
        travelling_salesman(
            initial_node="0", distances=distances, must_return_to_origin=False
        )
        == 14
    )
