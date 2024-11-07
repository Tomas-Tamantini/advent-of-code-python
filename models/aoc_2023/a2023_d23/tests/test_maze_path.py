import pytest
from ..logic import MazePath, MazeEdge


def test_maze_path_is_hashable():
    path_a = MazePath(("a", "b", "c"))
    path_b = MazePath(("a", "b", "c"))
    path_c = MazePath(("a", "c", "b"))
    assert hash(path_a) == hash(path_b)
    assert hash(path_a) != hash(path_c)
    assert path_a == path_b
    assert path_a != path_c


def test_maze_path_current_node_is_last_one():
    path = MazePath(("a", "b", "c"))
    assert path.current_node == "c"


def test_maze_path_checks_already_visited_nodes():
    path = MazePath(("a", "b", "c"))
    assert path.has_visited("b")
    assert not path.has_visited("z")


def test_maze_path_increments_path_and_weight():
    path = MazePath(("a", "b", "c"), total_weight=100)
    new_path = path.increment(new_node="d", weight_increment=20)
    assert new_path == MazePath(("a", "b", "c", "d"), total_weight=120)


def test_maze_path_keeps_track_of_number_of_nodes():
    path = MazePath(("a", "b", "c"), total_weight=100)
    assert path.num_nodes == 3


@pytest.mark.parametrize(
    "edge_start, edge_end, can_add",
    [("c", "d", True), ("x", "y", True), ("c", "a", False), ("z", "b", False)],
)
def test_can_add_edge_to_maze_path_if_it_does_not_form_cycle(
    edge_start, edge_end, can_add
):
    edge = MazeEdge(edge_start, edge_end, weight=1)
    path = MazePath(("a", "b", "c"), total_weight=100)
    assert can_add == path.can_add_edge(edge)
