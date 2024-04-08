from math import inf
from models.vectors import Vector2D
from models.aoc_2019.a2019_d18 import TunnelMazeGraph


def test_tunnel_maze_graph_connects_neighboring_nodes_with_weight_one():
    graph = TunnelMazeGraph()
    node_a = Vector2D(0, 0)
    node_b = Vector2D(1, 0)
    node_c = Vector2D(0, 1)
    graph.add_node(node_a)
    graph.add_node(node_b)
    graph.add_node(node_c)
    assert graph.weight(node_a, node_b) == 1
    assert graph.weight(node_a, node_c) == 1
    assert graph.weight(node_b, node_c) == inf


def test_reducing_tunnel_maze_graph_eliminates_nodes_with_one_or_two_neighbors():
    graph = TunnelMazeGraph()
    for i in range(3):
        for j in range(3):
            graph.add_node(Vector2D(i, j))
    assert graph.num_nodes == 9
    assert graph.weight(Vector2D(0, 1), Vector2D(1, 0)) == inf
    graph.reduce(irreducible_nodes=set())
    assert graph.num_nodes == 5
    assert graph.weight(Vector2D(0, 1), Vector2D(1, 0)) == 2


def test_reducing_tunnel_maze_graph_retains_irreducible_nodes():
    graph = TunnelMazeGraph()
    for i in range(3):
        for j in range(3):
            graph.add_node(Vector2D(i, j))
    graph.reduce(irreducible_nodes={Vector2D(0, 0)})
    assert graph.num_nodes == 6
    assert graph.weight(Vector2D(0, 1), Vector2D(1, 0)) == inf


def test_reducing_tunnel_maze_graph_happens_recursively():
    graph = TunnelMazeGraph()
    for i in range(11):
        graph.add_node(Vector2D(i, 0))
    graph.reduce(irreducible_nodes={Vector2D(0, 0), Vector2D(10, 0)})
    assert graph.num_nodes == 2
    assert graph.weight(Vector2D(0, 0), Vector2D(10, 0)) == 10


def test_tunnel_maze_graph_finds_shortest_distance_between_two_nodes():
    graph = TunnelMazeGraph()
    for i in range(3):
        for j in range(3):
            graph.add_node(Vector2D(i, j))
    graph.reduce(irreducible_nodes={Vector2D(0, 0)})
    origin = Vector2D(0, 0)
    destination = Vector2D(2, 1)
    forbidden_nodes = set()
    assert graph.shortest_distance(origin, destination, forbidden_nodes) == 3


def test_tunnel_maze_graph_shortest_distance_between_two_nodes_takes_forbidden_nodes_into_account():
    graph = TunnelMazeGraph()
    for i in range(3):
        for j in range(3):
            graph.add_node(Vector2D(i, j))
    graph.reduce(irreducible_nodes={Vector2D(0, 0)})
    origin = Vector2D(0, 0)
    destination = Vector2D(2, 1)
    forbidden_nodes = {Vector2D(1, 0), Vector2D(1, 1)}
    assert graph.shortest_distance(origin, destination, forbidden_nodes) == 5

    forbidden_nodes.add(Vector2D(1, 2))
    assert graph.shortest_distance(origin, destination, forbidden_nodes) == inf
