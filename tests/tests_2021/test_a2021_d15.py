from models.vectors import Vector2D
from models.char_grid import CharacterGrid
from models.aoc_2021 import UnderwaterCaveMaze


def _example_cave() -> UnderwaterCaveMaze:
    grid = CharacterGrid(
        text="""1163751742
                1381373672
                2136511328
                3694931569
                7463417111
                1319128137
                1359912421
                3125421639
                1293138521
                2311944581"""
    )
    return UnderwaterCaveMaze(
        risk_levels={pos: int(char) for pos, char in grid.tiles.items()}
    )


def test_underwater_cave_maze_has_risk_associated_with_each_position():
    maze = _example_cave()
    assert maze.risk_level_at(Vector2D(0, 0)) == 1
    assert maze.risk_level_at(Vector2D(2, 1)) == 8


def test_can_find_risk_level_of_shortest_path_between_two_points_in_underwater_cave_maze():
    maze = _example_cave()
    min_risk = maze.risk_of_optimal_path(start=Vector2D(0, 0), end=Vector2D(9, 9))
    assert min_risk == 40
