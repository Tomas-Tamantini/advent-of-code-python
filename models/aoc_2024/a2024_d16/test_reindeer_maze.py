import pytest

from models.common.io import CharacterGrid
from models.common.vectors import CardinalDirection, Vector2D

from .logic import ReindeerMaze


def test_reindeer_in_maze_spends_one_point_per_move_forward():
    maze = ReindeerMaze(
        start_tile=Vector2D(0, 0),
        start_direction=CardinalDirection.EAST,
        end_tile=Vector2D(10, 0),
        maze_tiles={Vector2D(i, 0) for i in range(11)},
    )
    assert maze.minimal_score() == 10


def test_reindeer_in_maze_spends_1000_points_per_90_degrees_turn():
    maze = ReindeerMaze(
        start_tile=Vector2D(0, 0),
        start_direction=CardinalDirection.NORTH,
        end_tile=Vector2D(10, 0),
        maze_tiles={Vector2D(i, 0) for i in range(11)},
    )
    assert maze.minimal_score() == 1010


_maze_a = """
          ###############
          #.......#....E#
          #.#.###.#.###.#
          #.....#.#...#.#
          #.###.#####.#.#
          #.#.#.......#.#
          #.#.#####.###.#
          #...........#.#
          ###.#.#####.#.#
          #...#.....#.#.#
          #.#.#.###.#.#.#
          #.....#...#.#.#
          #.###.#.#.#.#.#
          #S..#.....#...#
          ###############
          """

_maze_b = """
          #################
          #...#...#...#..E#
          #.#.#.#.#.#.#.#.#
          #.#.#.#...#...#.#
          #.#.#.#.###.#.#.#
          #...#.#.#.....#.#
          #.#.#.#.#.#####.#
          #.#...#.#.#.....#
          #.#.#####.#.###.#
          #.#.#.......#...#
          #.#.###.#####.###
          #.#.#...#.....#.#
          #.#.#.#####.###.#
          #.#.#.........#.#
          #.#.#.#########.#
          #S#.............#
          #################
          """


def _parse_maze(maze_str) -> ReindeerMaze:
    grid = CharacterGrid(maze_str)
    start_tile = next(grid.positions_with_value("S"))
    start_direction = CardinalDirection.EAST
    end_tile = next(grid.positions_with_value("E"))
    maze_tiles = set(grid.positions_with_value(".")) | {start_tile, end_tile}
    return ReindeerMaze(start_tile, start_direction, end_tile, maze_tiles)


@pytest.mark.parametrize(
    ("maze_str", "expected_score"), [(_maze_a, 7036), (_maze_b, 11048)]
)
def test_reindeer_completes_maze_with_minimal_score(maze_str, expected_score):
    maze = _parse_maze(maze_str)
    assert expected_score == maze.minimal_score()


@pytest.mark.parametrize(
    ("maze_str", "expected_num_tiles"), [(_maze_a, 45), (_maze_b, 64)]
)
def test_reindeer_maze_keeps_track_of_tiles_on_optimal_paths(
    maze_str, expected_num_tiles
):
    maze = _parse_maze(maze_str)
    assert expected_num_tiles == len(set(maze.tiles_on_optimal_paths()))
