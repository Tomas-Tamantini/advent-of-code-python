import pytest
from models.common.io import CharacterGrid
from models.common.vectors import Vector2D
from .logic import Gardener, BoundedGarden, InfiniteGarden

_GARDEN_STR = """...........
                 .....###.#.
                 .###.##..#.
                 ..#.#...#..
                 ....#.#....
                 .##..S####.
                 .##..#...#.
                 .......##..
                 .##.#.####.
                 .##..##.##.
                 ..........."""


def _initial_position() -> Vector2D:
    grid = CharacterGrid(_GARDEN_STR)
    return next(grid.positions_with_value("S"))


def _bounded_garden() -> BoundedGarden:
    grid = CharacterGrid(_GARDEN_STR)
    return BoundedGarden(
        width=grid.width,
        height=grid.height,
        rock_positions=set(grid.positions_with_value("#")),
    )


def _infinite_garden() -> InfiniteGarden:
    grid = CharacterGrid(_GARDEN_STR)
    return InfiniteGarden(
        width=grid.width,
        height=grid.height,
        rock_positions=set(grid.positions_with_value("#")),
    )


@pytest.mark.parametrize("valid_position", [Vector2D(0, 0), Vector2D(1, 1)])
def test_open_plot_in_bounded_garden_is_valid(valid_position):
    garden = _bounded_garden()
    assert garden.is_valid_position(valid_position)


@pytest.mark.parametrize("invalid_position", [Vector2D(1, 2), Vector2D(2, 2)])
def test_rock_plot_in_bounded_garden_is_invalid(invalid_position):
    garden = _bounded_garden()
    assert not garden.is_valid_position(invalid_position)


@pytest.mark.parametrize("invalid_position", [Vector2D(-1, 0), Vector2D(2, 11)])
def test_plot_outside_bounded_garden_is_invalid(invalid_position):
    garden = _bounded_garden()
    assert not garden.is_valid_position(invalid_position)


@pytest.mark.parametrize("valid_position", [Vector2D(0, 0), Vector2D(1, 1)])
def test_open_plot_in_infinite_garden_is_valid(valid_position):
    garden = _infinite_garden()
    assert garden.is_valid_position(valid_position)


@pytest.mark.parametrize("valid_position", [Vector2D(-1, 0), Vector2D(2, 11)])
def test_open_plot_outside_central_tile_of_infinite_garden_is_valid(valid_position):
    garden = _infinite_garden()
    assert garden.is_valid_position(valid_position)


@pytest.mark.parametrize("invalid_position", [Vector2D(1, 2), Vector2D(2, 11002)])
def test_rock_plot_in_infinite_garden_is_invalid(invalid_position):
    garden = _infinite_garden()
    assert not garden.is_valid_position(invalid_position)


def test_gardener_keeps_track_of_how_many_plots_they_could_reach_in_given_steps():
    gardener = Gardener(_initial_position())
    garden = _bounded_garden()
    series_generator = gardener.num_reachable_positions(garden)
    series = [next(series_generator) for _ in range(7)]
    assert series == [1, 2, 4, 6, 9, 13, 16]


def test_gardener_keeps_track_of_reachable_plots_in_efficent_manner():
    gardener = Gardener(_initial_position())
    garden = _infinite_garden()
    series_generator = gardener.num_reachable_positions(garden)
    series = [next(series_generator) for _ in range(101)]
    assert series[6] == 16
    assert series[10] == 50
    assert series[50] == 1594
    assert series[100] == 6536
    # assert series[500] == 167004
