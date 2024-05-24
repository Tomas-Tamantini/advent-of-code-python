from models.common.vectors import Vector2D
from models.common.io import CharacterGrid
from .hill_maze import HillMaze


def test_neighboring_hills_are_those_at_most_one_shorter_than_current():
    maze = HillMaze(
        grid=CharacterGrid(
            """
            abc
            acc
            ddd
            """
        )
    )
    neighbors = list(maze.neighbors(node=Vector2D(1, 1)))
    assert len(neighbors) == 3
    assert set(neighbors) == {Vector2D(2, 1), Vector2D(1, 0), Vector2D(1, 2)}


def test_hill_maze_finds_fastest_route_from_start_to_end():
    maze = HillMaze(
        grid=CharacterGrid(
            """
            Sabqponm
            abcryxxl
            accszExk
            acctuvwj
            abdefghi
            """
        )
    )
    assert maze.min_num_steps_to_destination("S", "E") == 31


def test_hill_maze_finds_fastest_route_to_any_cell_with_given_character():
    maze = HillMaze(
        grid=CharacterGrid(
            """
            Sabqponm
            abcryxxl
            accszExk
            acctuvwj
            abdefghi
            """
        )
    )
    assert maze.min_num_steps_to_destination("a", "E") == 29
