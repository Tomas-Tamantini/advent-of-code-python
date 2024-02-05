from models.vectors import Vector2D
from models.aoc_2018 import build_lattice_graph


def test_empty_regex_yields_graph_with_just_origin():
    assert list(build_lattice_graph("^$").nodes()) == [Vector2D(0, 0)]


def test_regex_with_single_direction_yields_graph_with_two_nodes_and_one_edge():
    graph = build_lattice_graph("^E$")

    assert list(graph.nodes()) == [Vector2D(0, 0), Vector2D(1, 0)]
    assert list(graph.neighbors(Vector2D(0, 0))) == [Vector2D(1, 0)]


def test_regex_with_branch_yields_multiple_paths():
    graph = build_lattice_graph("^E(N|S)W$")
    assert set(graph.nodes()) == {
        Vector2D(0, 0),
        Vector2D(1, 0),
        Vector2D(1, 1),
        Vector2D(1, -1),
        Vector2D(0, 1),
        Vector2D(0, -1),
    }
    assert list(graph.neighbors(Vector2D(0, 0))) == [Vector2D(1, 0)]


def test_branches_can_be_nested():
    graph = build_lattice_graph("^E(N|E(E||NN)S|S)E$")
    assert len(list(graph.nodes())) == 12
