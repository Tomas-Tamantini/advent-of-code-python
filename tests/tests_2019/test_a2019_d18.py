from math import inf
from models.vectors import Vector2D
from models.aoc_2019.a2019_d18 import TunnelMazeGraph, TunnelMaze, TunnelMazeExplorer


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


def test_tunnel_maze_explorer_is_sorted_by_distance_walked():
    explorer_a = TunnelMazeExplorer(position=Vector2D(0, 0), distance_walked=1)
    explorer_b = TunnelMazeExplorer(position=Vector2D(0, 0), distance_walked=2)
    assert explorer_a < explorer_b


def test_tunnel_maze_explorer_state_is_its_position_and_sorted_collected_keys():
    explorer = TunnelMazeExplorer(position=Vector2D(0, 0), collected_keys={"b", "a"})
    assert explorer.state() == (Vector2D(0, 0), ("a", "b"))


def test_tunnel_maze_explorer_can_move_to_next_key():
    explorer = TunnelMazeExplorer(
        position=Vector2D(10, 11), collected_keys={"b", "a"}, distance_walked=123
    )
    new_explorer = explorer.move_to_key(
        key_id="c", key_position=Vector2D(12, 13), distance=3
    )
    assert new_explorer.position == Vector2D(12, 13)
    assert new_explorer.collected_keys == {"a", "b", "c"}
    assert new_explorer.distance_walked == 126

    assert explorer.position == Vector2D(10, 11)
    assert explorer.collected_keys == {"a", "b"}
    assert explorer.distance_walked == 123


def _maze_from_string(maze_string: str) -> TunnelMaze:
    maze = TunnelMaze()
    for y, line in enumerate(maze_string.splitlines()):
        for x, char in enumerate(line):
            position = Vector2D(x, y)
            if char == ".":
                maze.add_open_passage(position)
            if char == "@":
                maze.set_entrance(position)
            if char.islower():
                maze.add_key(position, key_id=char)
            if char.isupper():
                maze.add_door(position, corresponding_key_id=char.lower())
    return maze


def test_tunnel_maze_makes_doors_keys_and_entrance_irreducible():
    maze = _maze_from_string(".@..a.A..")
    graph = maze.reduced_graph()
    assert graph.num_nodes == 3
    assert graph.weight(Vector2D(1, 0), Vector2D(4, 0)) == 3
    assert graph.weight(Vector2D(4, 0), Vector2D(6, 0)) == 2
    assert graph.weight(Vector2D(1, 0), Vector2D(6, 0)) == inf


def test_tunnel_maze_initializes_explorer_at_entrance():
    maze = TunnelMaze()
    maze.set_entrance(position=Vector2D(123, 456))
    explorer = maze.initial_explorer()
    assert explorer.position == Vector2D(123, 456)
    assert explorer.collected_keys == set()
    assert explorer.distance_walked == 0


def test_tunnel_maze_shortest_distance_to_all_keys_is_zero_if_no_keys():
    maze = _maze_from_string(".@.B.A..")
    assert maze.shortest_distance_to_all_keys() == 0


def test_tunnel_maze_shortest_distance_to_all_keys_takes_all_keys_into_account():
    maze = _maze_from_string(
        """
        a.C
        .@.
        ..b
        """
    )
    assert maze.shortest_distance_to_all_keys() == 6


def test_tunnel_maze_can_only_pass_through_door_if_corresponding_key_was_collected():
    maze = _maze_from_string(
        """
        ########################
        #f.D.E.e.C.b.A.@.a.B.c.#
        ######################.#
        #d.....................#
        ########################
        """
    )
    assert maze.shortest_distance_to_all_keys() == 86


def test_tunnel_maze_shortest_distance_to_all_keys_optimizes_path_through_maze():
    maze = _maze_from_string(
        """
        ########################
        #@..............ac.GI.b#
        ###d#e#f################
        ###A#B#C################
        ###g#h#i################
        ########################
        """
    )
    assert maze.shortest_distance_to_all_keys() == 81
