import pytest
from models.graphs import (
    min_path_length_with_bfs,
    explore_with_bfs,
    topological_sorting,
    travelling_salesman,
    UndirectedGraph,
    DirectedGraph,
    WeightedUndirectedGraph,
    WeightedDirectedGraph,
    dijkstra,
)


def test_mutable_undirected_graph_starts_empty():
    graph = UndirectedGraph()
    assert list(graph.nodes()) == []


def test_can_add_node_to_mutable_undirected_graph():
    graph = UndirectedGraph()
    graph.add_node("a")
    assert list(graph.nodes()) == ["a"]


def test_can_add_edge_to_mutable_undirected_graph():
    graph = UndirectedGraph()
    graph.add_edge("a", "b")
    assert set(graph.nodes()) == {"a", "b"}
    assert list(graph.neighbors("a")) == ["b"]
    assert list(graph.neighbors("b")) == ["a"]


def test_weighted_undirected_graph_starts_empty():
    graph = WeightedUndirectedGraph()
    assert list(graph.nodes()) == []


def test_can_add_node_to_weighted_undirected_graph():
    graph = WeightedUndirectedGraph()
    graph.add_node("a")
    assert list(graph.nodes()) == ["a"]


def test_can_add_weighted_edge_to_weighted_undirected_graph():
    graph = WeightedUndirectedGraph()
    graph.add_edge("a", "b", weight=2)
    assert set(graph.nodes()) == {"a", "b"}
    assert list(graph.neighbors("a")) == ["b"]
    assert list(graph.neighbors("b")) == ["a"]
    assert graph.weight("a", "b") == 2


def test_weight_between_non_adjacent_nodes_in_undirected_graph_is_infinity():
    graph = WeightedUndirectedGraph()
    graph.add_edge("a", "b", weight=2)
    assert graph.weight("a", "c") == float("inf")


def test_mutable_directed_graph_starts_empty():
    graph = DirectedGraph()
    assert list(graph.nodes()) == []


def test_can_add_node_to_mutable_directed_graph():
    graph = DirectedGraph()
    graph.add_node("a")
    assert list(graph.nodes()) == ["a"]


def test_can_add_edge_to_mutable_directed_graph():
    graph = DirectedGraph()
    graph.add_edge("a", "b")
    assert set(graph.nodes()) == {"a", "b"}
    assert list(graph.outgoing("a")) == ["b"]
    assert list(graph.incoming("b")) == ["a"]


def test_can_remove_node_from_mutable_directed_graph():
    graph = DirectedGraph()
    graph.add_edge("a", "b")
    graph.add_edge("b", "c")
    graph.remove_node("b")
    assert list(graph.nodes()) == ["a", "c"]
    assert list(graph.outgoing("a")) == []
    assert list(graph.incoming("c")) == []


def test_weighted_directed_graph_starts_empty():
    graph = WeightedDirectedGraph()
    assert list(graph.nodes()) == []


def test_can_add_node_to_weighted_directed_graph():
    graph = WeightedDirectedGraph()
    graph.add_node("a")
    assert list(graph.nodes()) == ["a"]


def test_can_add_weighted_edge_to_weighted_directed_graph():
    graph = WeightedDirectedGraph()
    graph.add_edge("a", "b", weight=2)
    assert set(graph.nodes()) == {"a", "b"}
    assert list(graph.outgoing("a")) == ["b"]
    assert list(graph.incoming("b")) == ["a"]
    assert list(graph.outgoing("b")) == []
    assert list(graph.incoming("a")) == []
    assert graph.weight("a", "b") == 2


def test_weight_between_non_adjacent_nodes_in_directed_graph_is_infinity():
    graph = WeightedDirectedGraph()
    graph.add_edge("a", "b", weight=2)
    assert set(graph.nodes()) == {"a", "b"}
    assert graph.weight("b", "a") == float("inf")


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
    dag = DirectedGraph()
    assert list(topological_sorting(dag)) == []


def test_topological_sorting_of_graph_with_single_node_contains_only_that_node():
    dag = DirectedGraph()
    dag.add_node("a")
    assert list(topological_sorting(dag)) == ["a"]


def test_topological_sorting_returns_nodes_in_topological_order():
    dag = DirectedGraph()
    dag.add_edge("b", "c")
    dag.add_edge("a", "b")
    dag.add_edge("b", "d")
    assert "".join(topological_sorting(dag)) in ("abcd", "abdc")


def test_topological_sorting_of_cyclical_graph_raises_error():
    dag = DirectedGraph()
    dag.add_edge("a", "b")
    dag.add_edge("b", "c")
    dag.add_edge("c", "a")

    with pytest.raises(ValueError):
        list(topological_sorting(dag))

    dag = DirectedGraph()
    dag.add_edge("a", "b")
    dag.add_edge("b", "c")
    dag.add_edge("c", "b")

    with pytest.raises(ValueError):
        list(topological_sorting(dag))


def test_topological_sorting_can_receive_tie_breaker():
    dag = DirectedGraph()
    dag.add_edge("C", "A")
    dag.add_edge("C", "F")
    dag.add_edge("A", "B")
    dag.add_edge("A", "D")
    dag.add_edge("B", "E")
    dag.add_edge("D", "E")
    dag.add_edge("F", "E")
    assert "".join(topological_sorting(dag, tie_breaker=lambda a, b: a < b)) == "CABDFE"


def test_dijkstra_raises_value_error_if_no_path():
    graph = WeightedUndirectedGraph()
    graph.add_edge("a", "b", weight=2)
    with pytest.raises(ValueError):
        dijkstra("a", "c", graph)


def test_dijkstra_returns_distance_zero_if_origin_equals_destination():
    graph = WeightedUndirectedGraph()
    graph.add_edge("a", "b", weight=2)
    path, distance = dijkstra("a", "a", graph)
    assert path == ["a"]
    assert distance == 0


def test_dijkstra_minimizes_distance():
    graph = WeightedUndirectedGraph()
    graph.add_edge("a", "b", weight=2)
    graph.add_edge("a", "c", weight=10)
    graph.add_edge("b", "d", weight=15)
    graph.add_edge("c", "d", weight=5)
    path, distance = dijkstra("a", "d", graph)
    assert path == ["a", "c", "d"]
    assert distance == 15


def test_dijkstra_finds_optimal_distance_even_if_multiple_optimal_paths():
    graph = WeightedUndirectedGraph()
    graph.add_edge("a", "b", weight=3)
    graph.add_edge("a", "d", weight=8)
    graph.add_edge("b", "d", weight=5)
    graph.add_edge("b", "e", weight=6)
    graph.add_edge("d", "e", weight=3)
    graph.add_edge("d", "f", weight=2)
    graph.add_edge("e", "f", weight=1)
    graph.add_edge("e", "c", weight=9)
    graph.add_edge("f", "c", weight=3)
    _, distance = dijkstra("a", "c", graph)
    assert distance == 13
