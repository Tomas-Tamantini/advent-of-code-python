from models.common.io import CharacterGrid
from models.common.vectors import Vector2D

from ..logic import max_length_non_repeating_path
from ..parser import parse_forest_map

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


def test_parse_forest_map_can_consider_or_ignore_slopes():
    start = Vector2D(1, 0)
    grid = CharacterGrid(_MAZE)
    slope_maze = parse_forest_map(grid, consider_slopes=True)
    flat_maze = parse_forest_map(grid, consider_slopes=False)
    end = Vector2D(x=21, y=22)
    slope_maze.reduce(irreducible_nodes={start, end})
    flat_maze.reduce(irreducible_nodes={start, end})
    assert 94 == max_length_non_repeating_path(slope_maze, start, end)
    assert 154 == max_length_non_repeating_path(flat_maze, start, end)
