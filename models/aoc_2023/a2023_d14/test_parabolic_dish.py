from models.common.io import CharacterGrid
from models.common.vectors import Vector2D, CardinalDirection
from .parabolic_dish import ParabolicDish


def _build_dish(dish_str: str) -> ParabolicDish:
    grid = CharacterGrid(dish_str)
    return ParabolicDish(
        width=grid.width,
        height=grid.height,
        cube_rocks=set(grid.positions_with_value("#")),
    )


def _rounded_rocks_positions(dish_str: str) -> set[Vector2D]:
    grid = CharacterGrid(dish_str)
    return set(grid.positions_with_value("O"))


def test_zero_rounded_rocks_as_input_yield_zero_rounded_rocks_as_output():
    dish = _build_dish(".")
    no_rocks = set()
    assert set(dish.tilt(no_rocks, CardinalDirection.EAST)) == set()


def test_rounded_rock_rolls_until_end_of_parabolic_dish_if_no_obstacles():
    dish_repr = """...
                   ...
                   ...
                   ..."""
    dish = _build_dish(dish_repr)
    rounded_rocks = {Vector2D(1, 2)}
    assert set(dish.tilt(rounded_rocks, CardinalDirection.NORTH)) == {Vector2D(1, 0)}
    assert set(dish.tilt(rounded_rocks, CardinalDirection.SOUTH)) == {Vector2D(1, 3)}
    assert set(dish.tilt(rounded_rocks, CardinalDirection.EAST)) == {Vector2D(2, 2)}
    assert set(dish.tilt(rounded_rocks, CardinalDirection.WEST)) == {Vector2D(0, 2)}


def test_rounded_rocks_are_obstacles_to_each_other():
    dish_repr = """...
                   ...
                   ...
                   ..."""
    dish = _build_dish(dish_repr)
    rounded_rocks = {Vector2D(0, 1), Vector2D(0, 2), Vector2D(1, 1)}
    assert set(dish.tilt(rounded_rocks, CardinalDirection.NORTH)) == {
        Vector2D(0, 0),
        Vector2D(0, 1),
        Vector2D(1, 0),
    }
    assert set(dish.tilt(rounded_rocks, CardinalDirection.SOUTH)) == {
        Vector2D(0, 2),
        Vector2D(0, 3),
        Vector2D(1, 3),
    }
    assert set(dish.tilt(rounded_rocks, CardinalDirection.EAST)) == {
        Vector2D(1, 1),
        Vector2D(2, 2),
        Vector2D(2, 1),
    }
    assert set(dish.tilt(rounded_rocks, CardinalDirection.WEST)) == {
        Vector2D(0, 1),
        Vector2D(0, 2),
        Vector2D(1, 1),
    }


def test_cube_rocks_are_obstacles_to_rounded_rocks():
    dish_repr = """#..
                   ...
                   .#.
                   ..."""
    dish = _build_dish(dish_repr)
    rounded_rocks = {Vector2D(0, 1), Vector2D(0, 2), Vector2D(1, 1)}
    assert set(dish.tilt(rounded_rocks, CardinalDirection.NORTH)) == {
        Vector2D(0, 1),
        Vector2D(0, 2),
        Vector2D(1, 0),
    }
    assert set(dish.tilt(rounded_rocks, CardinalDirection.SOUTH)) == {
        Vector2D(0, 2),
        Vector2D(0, 3),
        Vector2D(1, 1),
    }
    assert set(dish.tilt(rounded_rocks, CardinalDirection.EAST)) == {
        Vector2D(1, 1),
        Vector2D(0, 2),
        Vector2D(2, 1),
    }
    assert set(dish.tilt(rounded_rocks, CardinalDirection.WEST)) == {
        Vector2D(0, 1),
        Vector2D(0, 2),
        Vector2D(1, 1),
    }


_EXAMPLE_DISH = """O....#....
                   O.OO#....#
                   .....##...
                   OO.#O....O
                   .O.....O#.
                   O.#..O.#.#
                   ..O..#O..O
                   .......O..
                   #....###..
                   #OO..#...."""


def test_parabolic_dish_load_is_calculated_from_south_edge():
    dish = _build_dish(_EXAMPLE_DISH)
    rocks = _rounded_rocks_positions(_EXAMPLE_DISH)
    rolled_rocks = dish.tilt(rocks, CardinalDirection.NORTH)
    assert dish.load_from_south_edge(rolled_rocks) == 136
