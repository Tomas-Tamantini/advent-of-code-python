from models.common.vectors import Vector2D
from models.common.io import CharacterGrid
from ..falling_sand import FallingSand


def test_falling_sand_with_no_obstacle_never_rests():
    falling_sand = FallingSand(
        sand_pour_position=Vector2D(123, 0), obstacle_positions=set()
    )
    falling_sand.pour_until_steady_state()
    assert falling_sand.resting_sand_positions == set()


def test_sand_without_obstacle_directly_underneath_never_rests():
    falling_sand = FallingSand(
        sand_pour_position=Vector2D(5, 0),
        obstacle_positions={Vector2D(4, 10), Vector2D(6, 10)},
    )
    falling_sand.pour_until_steady_state()
    assert falling_sand.resting_sand_positions == set()


def test_sand_without_obstacle_down_and_to_the_left_never_rests():
    falling_sand = FallingSand(
        sand_pour_position=Vector2D(5, 0),
        obstacle_positions={Vector2D(5, 10), Vector2D(6, 10)},
    )
    falling_sand.pour_until_steady_state()
    assert falling_sand.resting_sand_positions == set()


def test_sand_without_obstacle_down_and_to_the_right_never_rests():
    falling_sand = FallingSand(
        sand_pour_position=Vector2D(5, 0),
        obstacle_positions={Vector2D(5, 10), Vector2D(4, 10)},
    )
    falling_sand.pour_until_steady_state()
    assert falling_sand.resting_sand_positions == set()


def test_sand_without_obstacle_in_all_three_possible_downward_cells_rests():
    falling_sand = FallingSand(
        sand_pour_position=Vector2D(5, 0),
        obstacle_positions={Vector2D(4, 10), Vector2D(5, 10), Vector2D(6, 10)},
    )
    falling_sand.pour_until_steady_state()
    assert falling_sand.resting_sand_positions == {Vector2D(5, 9)}


def test_pouring_sand_piles_on_top_of_one_another():
    falling_sand = FallingSand(
        sand_pour_position=Vector2D(3, 0),
        obstacle_positions={Vector2D(i, 10) for i in range(7)},
    )
    falling_sand.pour_until_steady_state()
    assert falling_sand.resting_sand_positions == {
        Vector2D(1, 9),
        Vector2D(2, 9),
        Vector2D(3, 9),
        Vector2D(4, 9),
        Vector2D(5, 9),
        Vector2D(2, 8),
        Vector2D(3, 8),
        Vector2D(4, 8),
        Vector2D(3, 7),
    }


def test_pouring_sand_piles_even_in_complicated_obstacles():
    grid = CharacterGrid(
        """
        ......+...
        ..........
        ..........
        ..........
        ....#...##
        ....#...#.
        ..###...#.
        ........#.
        ........#.
        #########.
        """
    )
    obstacles = set(grid.positions_with_value("#"))
    sand_pour_position = next(grid.positions_with_value("+"))
    falling_sand = FallingSand(sand_pour_position, obstacles)
    falling_sand.pour_until_steady_state()
    assert len(falling_sand.resting_sand_positions) == 24
