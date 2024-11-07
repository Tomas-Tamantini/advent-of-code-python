from math import inf
from models.common.graphs import WeightedDirectedGraph
from ..logic import MazeExplorer, MazePath


def test_objective_value_on_maze_path_is_path_weight_if_current_node_is_destination():
    graph = WeightedDirectedGraph()
    explorer = MazeExplorer(graph, end_node="c")
    path = MazePath(
        current_node="c", previously_visited=frozenset({"a", "b"}), total_weight=123
    )
    assert explorer.objective_value(path) == 123


def test_objective_value_on_maze_path_is_path_minus_inf_if_current_node_is_not_destination():
    graph = WeightedDirectedGraph()
    explorer = MazeExplorer(graph, end_node="d")
    path = MazePath(current_node="c", previously_visited=frozenset({"a", "b"}))
    assert explorer.objective_value(path) == -inf


def test_upper_bound_on_maze_path_length_is_length_itself_if_current_node_is_destination():
    graph = WeightedDirectedGraph()
    explorer = MazeExplorer(graph, end_node="c")
    path = MazePath(
        current_node="c", previously_visited=frozenset({"a", "b"}), total_weight=123
    )
    assert explorer.upper_bound_on_objective_value(path) == 123


def test_upper_bound_on_maze_path_is_path_length_if_single_path():
    graph = WeightedDirectedGraph()
    graph.add_edge("a", "b", weight=100)
    graph.add_edge("b", "c", weight=10)
    graph.add_edge("c", "d", weight=20)
    explorer = MazeExplorer(graph, end_node="d")
    path = MazePath(
        current_node="b", previously_visited=frozenset({"a"}), total_weight=100
    )
    assert explorer.upper_bound_on_objective_value(path) == 130


def test_upper_bound_on_maze_path_is_sum_of_largest_remaining_edges():
    graph = WeightedDirectedGraph()

    graph.add_edge("a", "b", 1000)
    graph.add_edge("b", "c", 1)
    graph.add_edge("d", "e", 2)
    graph.add_edge("e", "f", 3)
    graph.add_edge("g", "h", 4)
    graph.add_edge("h", "i", 5)

    graph.add_edge("a", "d", 9000)
    graph.add_edge("b", "e", 1)
    graph.add_edge("c", "f", 10)
    graph.add_edge("d", "g", 20)
    graph.add_edge("e", "h", 30)
    graph.add_edge("f", "i", 40)

    explorer = MazeExplorer(graph, end_node="i")
    path = MazePath(
        current_node="b", previously_visited=frozenset({"a"}), total_weight=1000
    )
    assert explorer.upper_bound_on_objective_value(path) == 1112


def test_maze_path_has_no_neighboring_states_if_current_node_is_destination():
    graph = WeightedDirectedGraph()
    explorer = MazeExplorer(graph, end_node="c")
    path = MazePath(
        current_node="c", previously_visited=frozenset({"a", "b"}), total_weight=123
    )
    assert list(explorer.children_states(path)) == []


def test_maze_path_has_path_incremented_by_one_step_as_neighbors():
    graph = WeightedDirectedGraph()
    graph.add_edge("c", "d", weight=123)
    graph.add_edge("c", "e", weight=321)
    graph.add_edge("f", "c", weight=567)
    graph.add_edge("c", "a", weight=789)
    explorer = MazeExplorer(graph, end_node="z")
    path = MazePath(
        current_node="c", previously_visited=frozenset({"a", "b"}), total_weight=1000
    )
    neighbors = list(explorer.children_states(path))
    assert len(neighbors) == 2
    assert set(neighbors) == {
        MazePath(
            current_node="d",
            previously_visited=frozenset({"a", "b", "c"}),
            total_weight=1123,
        ),
        MazePath(
            current_node="e",
            previously_visited=frozenset({"a", "b", "c"}),
            total_weight=1321,
        ),
    }
