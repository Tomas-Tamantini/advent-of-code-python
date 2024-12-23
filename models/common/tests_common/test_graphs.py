from math import inf

import pytest

from models.common.graphs import (
    DirectedGraph,
    DisjointSet,
    GridMaze,
    Maze,
    UndirectedGraph,
    WeightedDirectedGraph,
    WeightedUndirectedGraph,
    a_star,
    dijkstra,
    explore_with_bfs,
    min_path_length_with_bfs,
    topological_sorting,
    travelling_salesman,
)
from models.common.vectors import Vector2D


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


def test_can_check_connections_in_mutable_undirected_graph():
    graph = UndirectedGraph()
    graph.add_edge("a", "b")
    graph.add_edge("b", "c")
    assert graph.are_connected("a", "b")
    assert graph.are_connected("b", "a")
    assert not graph.are_connected("a", "c")


def test_mutable_undirected_graph_keeps_track_of_number_of_nodes():
    graph = UndirectedGraph()
    assert graph.num_nodes == 0
    graph.add_node("a")
    assert graph.num_nodes == 1
    graph.add_edge("a", "b")
    assert graph.num_nodes == 2


def test_weighted_undirected_graph_starts_empty():
    graph = WeightedUndirectedGraph()
    assert list(graph.nodes()) == []


def test_can_add_node_to_weighted_undirected_graph():
    graph = WeightedUndirectedGraph()
    graph.add_node("a")
    assert list(graph.nodes()) == ["a"]


def test_distance_between_node_and_itself_is_zero_in_weighted_undirected_graph():
    graph = WeightedUndirectedGraph()
    graph.add_node("a")
    assert graph.weight("a", "a") == 0


def test_can_remove_node_from_weighted_undirected_graph():
    graph = WeightedUndirectedGraph()
    graph.add_edge("a", "b", 123)
    graph.remove_node("a")
    assert list(graph.nodes()) == ["b"]
    assert list(graph.neighbors("b")) == []


def test_can_add_weighted_edge_to_weighted_undirected_graph():
    graph = WeightedUndirectedGraph()
    graph.add_edge("a", "b", weight=2)
    assert set(graph.nodes()) == {"a", "b"}
    assert list(graph.neighbors("a")) == ["b"]
    assert list(graph.neighbors("b")) == ["a"]
    assert graph.has_edge("a", "b")
    assert graph.weight("a", "b") == 2


def test_weight_between_non_adjacent_nodes_in_undirected_graph_is_infinity():
    graph = WeightedUndirectedGraph()
    graph.add_edge("a", "b", weight=2)
    assert not graph.has_edge("a", "c")
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


def test_neighbors_in_directed_graph_are_from_outgoing_edges_only():
    graph = DirectedGraph()
    graph.add_edge("a", "b")
    assert set(graph.nodes()) == {"a", "b"}
    assert list(graph.neighbors("a")) == ["b"]
    assert list(graph.neighbors("b")) == []


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


def test_neighbors_in_weighted_directed_graph_are_from_outgoing_edges_only():
    graph = WeightedDirectedGraph()
    graph.add_edge("a", "b", weight=2)
    assert set(graph.nodes()) == {"a", "b"}
    assert list(graph.neighbors("a")) == ["b"]
    assert list(graph.neighbors("b")) == []


def test_weighted_directed_graph_keeps_track_of_number_of_nodes():
    graph = WeightedDirectedGraph()
    assert graph.num_nodes == 0
    graph.add_edge("a", "b", weight=2)
    assert graph.num_nodes == 2


class MockGraph:
    @staticmethod
    def neighbors(node):
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
    assert "".join(topological_sorting(dag)) in {"abcd", "abdc"}


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


def test_dijkstra_also_works_with_single_method_weighted_graph():
    class _SingleMethod:
        @staticmethod
        def weighted_neighbors(node):
            yield "b", 2
            yield "c", 10

    path, distance = dijkstra("a", "c", _SingleMethod())
    assert path == ["a", "c"]
    assert distance == 10


class _MockAStarGraph(WeightedUndirectedGraph):
    @staticmethod
    def heuristic_potential(node) -> float:
        # Taken from computerphile video https://www.youtube.com/watch?v=ySN5Wnu88nE
        return {
            "S": 10,
            "A": 9,
            "B": 7,
            "C": 8,
            "D": 8,
            "E": 0,
            "F": 6,
            "G": 3,
            "H": 6,
            "I": 4,
            "J": 4,
            "K": 3,
            "L": 6,
        }[node]


def test_a_star_raises_value_error_if_no_path():
    graph = _MockAStarGraph()
    graph.add_edge("A", "B", weight=2)
    with pytest.raises(ValueError):
        a_star("A", is_destination=lambda n: n == "C", graph=graph)


def test_a_star_returns_distance_zero_if_origin_equals_destination():
    graph = _MockAStarGraph()
    graph.add_edge("a", "b", weight=2)
    path, distance = a_star("a", is_destination=lambda n: n == "a", graph=graph)
    assert path == ["a"]
    assert distance == 0


def test_a_star_returns_path_with_optimal_distance():
    graph = _MockAStarGraph()
    # Taken from computerphile video https://www.youtube.com/watch?v=ySN5Wnu88nE
    graph.add_edge("S", "A", 7)
    graph.add_edge("S", "B", 2)
    graph.add_edge("S", "C", 3)
    graph.add_edge("A", "B", 3)
    graph.add_edge("A", "D", 4)
    graph.add_edge("B", "D", 4)
    graph.add_edge("B", "H", 1)
    graph.add_edge("C", "L", 2)
    graph.add_edge("L", "I", 4)
    graph.add_edge("L", "J", 4)
    graph.add_edge("I", "J", 6)
    graph.add_edge("I", "K", 4)
    graph.add_edge("J", "K", 4)
    graph.add_edge("K", "E", 5)
    graph.add_edge("D", "F", 5)
    graph.add_edge("H", "F", 3)
    graph.add_edge("H", "G", 2)
    graph.add_edge("G", "E", 2)

    path, distance = a_star("S", is_destination=lambda n: n == "E", graph=graph)
    assert path == ["S", "B", "H", "G", "E"]
    assert distance == 7


def test_disjoint_set_starts_empty():
    disjoint_set = DisjointSet()
    assert disjoint_set.num_sets == 0


def test_can_make_set_in_disjoint_set():
    disjoint_set = DisjointSet()
    disjoint_set.make_set("a")
    assert disjoint_set.num_sets == 1


def test_can_merge_sets_in_disjoint_set():
    disjoint_set = DisjointSet()
    disjoint_set.make_set("a")
    disjoint_set.make_set("b")
    assert disjoint_set.num_sets == 2
    disjoint_set.union("a", "b")
    assert disjoint_set.num_sets == 1


def test_finding_element_in_set_returns_root():
    disjoint_set = DisjointSet()
    disjoint_set.make_set("a")
    disjoint_set.make_set("b")
    disjoint_set.union("a", "b")
    assert disjoint_set.find("a") == disjoint_set.find("b")


def test_finding_element_which_does_not_exist_raises_key_error():
    disjoint_set = DisjointSet()
    disjoint_set.make_set("a")
    with pytest.raises(KeyError):
        disjoint_set.find("b")


def _example_3x3_maze():
    maze = Maze()
    for i in range(3):
        for j in range(3):
            current_node = Vector2D(i, j)
            if i < 2:
                node_right = Vector2D(i + 1, j)
                maze.add_edge(current_node, node_right, weight=1)
            if j < 2:
                node_down = Vector2D(i, j + 1)
                maze.add_edge(current_node, node_down, weight=1)
    return maze


def test_reducing_maze_eliminates_nodes_with_one_or_two_neighbors():
    graph = _example_3x3_maze()
    assert graph.num_nodes == 9
    assert graph.weight(Vector2D(0, 1), Vector2D(1, 0)) == inf
    graph.reduce(irreducible_nodes=set())
    assert graph.num_nodes == 5
    assert graph.weight(Vector2D(0, 1), Vector2D(1, 0)) == 2


def test_reducing_maze_retains_irreducible_nodes():
    graph = _example_3x3_maze()
    graph.reduce(irreducible_nodes={Vector2D(0, 0)})
    assert graph.num_nodes == 6
    assert graph.weight(Vector2D(0, 1), Vector2D(1, 0)) == inf


def test_reducing_maze_happens_recursively():
    graph = Maze()
    for i in range(10):
        graph.add_edge(Vector2D(i, 0), Vector2D(i + 1, 0), weight=1)
    graph.reduce(irreducible_nodes={Vector2D(0, 0), Vector2D(10, 0)})
    assert graph.num_nodes == 2
    assert graph.weight(Vector2D(0, 0), Vector2D(10, 0)) == 10


def test_maze_finds_shortest_distance_between_two_nodes():
    graph = _example_3x3_maze()
    graph.reduce(irreducible_nodes={Vector2D(0, 0)})
    origin = Vector2D(0, 0)
    destination = Vector2D(2, 1)
    assert graph.shortest_distance(origin, destination) == 3


def test_grid_maze_connects_adjacent_cells_nodes_with_weight_one():
    graph = GridMaze()
    node_a = Vector2D(0, 0)
    node_b = Vector2D(1, 0)
    node_c = Vector2D(0, 1)
    graph.add_node_and_connect_to_neighbors(node_a)
    graph.add_node_and_connect_to_neighbors(node_b)
    graph.add_node_and_connect_to_neighbors(node_c)
    assert graph.weight(node_a, node_b) == 1
    assert graph.weight(node_a, node_c) == 1
    assert graph.weight(node_b, node_c) == inf
