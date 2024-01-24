import pytest
from models.graphs import (
    min_path_length_with_bfs,
    explore_with_bfs,
    topological_sorting,
    travelling_salesman,
    MutableDirectedGraph,
)


def test_mutable_directed_graph_starts_empty():
    graph = MutableDirectedGraph()
    assert list(graph.nodes()) == []


def test_can_add_node_to_mutable_directed_graph():
    graph = MutableDirectedGraph()
    graph.add_node("a")
    assert list(graph.nodes()) == ["a"]


def test_can_add_edge_to_mutable_directed_graph():
    graph = MutableDirectedGraph()
    graph.add_edge("a", "b")
    assert set(graph.nodes()) == {"a", "b"}
    assert list(graph.outgoing("a")) == ["b"]
    assert list(graph.incoming("b")) == ["a"]


class MockGraph:
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
    assert (
        min_path_length_with_bfs(
            graph,
            initial_node="final",
            is_final_state=lambda n: n == "final",
        )
        == 0
    )


def test_if_no_path_to_final_state_then_raise_value_error():
    with pytest.raises(ValueError):
        min_path_length_with_bfs(
            graph,
            initial_node="f",
            is_final_state=lambda n: n == "final",
        )


def test_minimum_path_from_initial_to_final_node_is_found():
    assert (
        min_path_length_with_bfs(
            graph,
            initial_node="a",
            is_final_state=lambda n: n == "final",
        )
        == 2
    )


def test_can_explore_graph_with_bfs():
    assert list(explore_with_bfs(graph, initial_node="a")) == [
        ("a", 0),
        ("b", 1),
        ("c", 1),
        ("d", 1),
        ("final", 2),
    ]


def test_travelling_salesman_of_single_city_is_zero():
    assert (
        travelling_salesman(
            initial_node="0",
            distances={},
            must_return_to_origin=False,
        )
        == 0
    )


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


def test_topological_sorting_of_empty_graph_is_empty():
    dag = MutableDirectedGraph()
    assert list(topological_sorting(dag)) == []


def test_topological_sorting_of_graph_with_single_node_contains_only_that_node():
    dag = MutableDirectedGraph()
    dag.add_node("a")
    assert list(topological_sorting(dag)) == ["a"]


def test_topological_sorting_returns_nodes_in_topological_order():
    dag = MutableDirectedGraph()
    dag.add_edge("b", "c")
    dag.add_edge("a", "b")
    dag.add_edge("b", "d")
    assert "".join(topological_sorting(dag)) in ("abcd", "abdc")


def test_topological_sorting_of_cyclical_graph_raises_error():
    dag = MutableDirectedGraph()
    dag.add_edge("a", "b")
    dag.add_edge("b", "c")
    dag.add_edge("c", "a")

    with pytest.raises(ValueError):
        list(topological_sorting(dag))

    dag = MutableDirectedGraph()
    dag.add_edge("a", "b")
    dag.add_edge("b", "c")
    dag.add_edge("c", "b")

    with pytest.raises(ValueError):
        list(topological_sorting(dag))


def test_topological_sorting_can_receive_tie_breaker():
    dag = MutableDirectedGraph()
    dag.add_edge("C", "A")
    dag.add_edge("C", "F")
    dag.add_edge("A", "B")
    dag.add_edge("A", "D")
    dag.add_edge("B", "E")
    dag.add_edge("D", "E")
    dag.add_edge("F", "E")
    assert "".join(topological_sorting(dag, tie_breaker=lambda a, b: a < b)) == "CABDFE"
