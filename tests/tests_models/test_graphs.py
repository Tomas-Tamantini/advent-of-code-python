from models.graphs import min_path_length_with_bfs, explore_with_bfs
import pytest
from dataclasses import dataclass


@dataclass(frozen=True)
class MockNode:
    id: str

    def is_final_state(self):
        return self.id == "final"

    def neighboring_valid_states(self):
        adjacencies = {
            "a": ("b", "c", "d"),
            "b": ("a", "d"),
            "c": ("final", "b"),
            "d": ("c",),
            "final": tuple(),
            "e": ("f",),
            "f": ("e",),
        }
        return (MockNode(id) for id in adjacencies[self.id])


def test_if_initial_node_is_final_state_then_min_path_is_zero():
    initial_node = MockNode("final")
    assert min_path_length_with_bfs(initial_node) == 0


def test_if_no_path_to_final_state_then_raise_value_error():
    initial_node = MockNode("f")
    with pytest.raises(ValueError):
        min_path_length_with_bfs(initial_node)


def test_minimum_path_from_initial_to_final_node_is_found():
    initial_node = MockNode("a")
    assert min_path_length_with_bfs(initial_node) == 2


def test_can_explore_graph_with_bfs():
    initial_node = MockNode("a")
    assert list(explore_with_bfs(initial_node)) == [
        (MockNode("a"), 0),
        (MockNode("b"), 1),
        (MockNode("c"), 1),
        (MockNode("d"), 1),
        (MockNode("final"), 2),
    ]
