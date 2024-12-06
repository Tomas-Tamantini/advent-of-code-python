from math import inf

import pytest

from models.common.io import CharacterGrid
from models.common.vectors import CardinalDirection, Vector2D

from ..logic import DirectedMaze, max_length_non_repeating_path


def _parse_maze(maze_str: str) -> DirectedMaze:
    grid = CharacterGrid(maze_str)
    maze = DirectedMaze()
    for undirected_tile in grid.positions_with_value("."):
        maze.add_tile(undirected_tile)
    symbols = {
        "^": CardinalDirection.NORTH,
        ">": CardinalDirection.EAST,
        "v": CardinalDirection.SOUTH,
        "<": CardinalDirection.WEST,
    }
    for symbol, direction in symbols.items():
        for tile in grid.positions_with_value(symbol):
            maze.add_tile(tile, direction)
    return maze


def test_directed_maze_has_path_from_start_to_finish():
    maze = DirectedMaze()
    start = Vector2D(0, 0)
    end = Vector2D(0, 1)
    maze.add_tile(start)
    maze.add_tile(end)
    assert 1 == max_length_non_repeating_path(maze, start, end)


def test_directed_maze_can_have_directed_tiles():
    maze = DirectedMaze()
    start = Vector2D(0, 0)
    end = Vector2D(0, 2)
    maze.add_tile(start)
    maze.add_tile(Vector2D(0, 1), tile_direction=CardinalDirection.NORTH)
    maze.add_tile(end)
    assert -inf == max_length_non_repeating_path(maze, start, end)


def test_directed_maze_can_have_multiple_paths():
    maze = _parse_maze(
        """.>.
           .#.
           .>.
           .#.
           .<."""
    )

    start = Vector2D(0, 0)
    end = Vector2D(2, 0)

    assert 6 == max_length_non_repeating_path(maze, start, end)


def test_directed_maze_can_be_reduced():
    maze = _parse_maze(
        """.>.
           .#.
           .>.
           .#.
           .<.
           .##"""
    )
    start = Vector2D(0, 0)
    end = Vector2D(2, 0)
    maze.reduce(irreducible_nodes={start, end})
    assert maze.weight(start, end) == 6
    assert maze.weight(end, start) == 10


_MAZE = """
        #.#####################
        #.......#########...###
        #######.#########.#.###
        ###.....#.>.>.###.#.###
        ###v#####.#v#.###.#.###
        ###.>...#.#.#.....#...#
        ###v###.#.#.#########.#
        ###...#.#.#.......#...#
        #####.#.#.#######.#.###
        #.....#.#.#.......#...#
        #.#####.#.#.#########v#
        #.#...#...#...###...>.#
        #.#.#v#######v###.###v#
        #...#.>.#...>.>.#.###.#
        #####v#.#.###v#.#.###.#
        #.....#...#...#.#.#...#
        #.#########.###.#.#.###
        #...###...#...#...#.###
        ###.###.#.###v#####v###
        #...#...#.#.>.>.#.>.###
        #.###.###.#.###.#.#v###
        #.....###...###...#...#
        #####################.#"""


def _directed_maze() -> DirectedMaze:
    return _parse_maze(_MAZE)


def _undirected_maze() -> DirectedMaze:
    maze_str = _MAZE
    for symbol in "^>v<":
        maze_str = maze_str.replace(symbol, ".")
    return _parse_maze(maze_str)


@pytest.mark.parametrize(
    ("maze", "path_length"), [(_directed_maze(), 94), (_undirected_maze(), 154)]
)
def test_reduced_directed_maze_finds_path_efficiently(maze, path_length):
    start = Vector2D(1, 0)
    end = Vector2D(x=21, y=22)
    maze.reduce(irreducible_nodes={start, end})
    assert path_length == max_length_non_repeating_path(maze, start, end)
