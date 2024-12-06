from models.common.vectors import Vector2D

from ..donut_maze import PortalMaze, RecursiveDonutMaze


def test_portal_maze_finds_shortest_path_between_entrance_and_exit():
    maze = PortalMaze()
    maze_cells = [(0, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
    for cell in maze_cells:
        maze.add_node_and_connect_to_neighbors(Vector2D(*cell))
    maze.set_entrance(Vector2D(0, 0))
    maze.set_exit(Vector2D(1, 2))
    assert maze.num_steps_to_solve() == 3


def test_portal_maze_can_have_portals_between_non_neighboring_nodes():
    maze = PortalMaze()
    for i in range(10):
        maze.add_node_and_connect_to_neighbors(Vector2D(0, i))
    maze.set_entrance(Vector2D(0, 0))
    maze.set_exit(Vector2D(0, 9))
    maze.add_portal(Vector2D(0, 2), Vector2D(0, 7))
    assert maze.num_steps_to_solve() == 5


def test_recursive_donut_maze_finds_shortest_path_between_entrance_and_exit():
    maze = RecursiveDonutMaze()
    maze_cells = [(0, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
    for cell in maze_cells:
        maze.add_node(Vector2D(*cell))
    maze.set_entrance(Vector2D(0, 0))
    maze.set_exit(Vector2D(1, 2))
    assert maze.num_steps_to_solve() == 3


def test_recursive_donut_maze_has_portals_to_allow_passage_between_levels():
    maze = RecursiveDonutMaze()
    for i in range(5):
        for j in range(3):
            maze.add_node(Vector2D(i, 100 * j))

    maze.set_entrance(Vector2D(0, 0))
    maze.set_exit(Vector2D(3, 200))
    maze.add_portal(step_up=Vector2D(2, 0), step_down=Vector2D(1, 100))
    maze.add_portal(step_up=Vector2D(0, 100), step_down=Vector2D(4, 200))
    maze.add_portal(step_up=Vector2D(0, 200), step_down=Vector2D(4, 100))
    assert maze.num_steps_to_solve() == 10
