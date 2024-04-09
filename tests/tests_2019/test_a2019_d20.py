from models.vectors import Vector2D
from models.aoc_2019.a2019_d20 import PortalMaze


def test_portal_maze_finds_shortest_path_between_entrance_and_exit():
    maze = PortalMaze()
    maze_cells = [(0, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
    for cell in maze_cells:
        maze.add_node(Vector2D(*cell))
    maze.set_entrance(Vector2D(0, 0))
    maze.set_exit(Vector2D(1, 2))
    assert maze.num_steps_to_solve() == 3


def test_portal_maze_can_have_portals_between_non_neighboring_nodes():
    maze = PortalMaze()
    for i in range(10):
        maze.add_node(Vector2D(0, i))
    maze.set_entrance(Vector2D(0, 0))
    maze.set_exit(Vector2D(0, 9))
    maze.add_portal(Vector2D(0, 2), Vector2D(0, 7))
    assert maze.num_steps_to_solve() == 5
