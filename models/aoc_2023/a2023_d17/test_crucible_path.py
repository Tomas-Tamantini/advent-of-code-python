import pytest
from models.common.io import CharacterGrid
from models.common.vectors import Vector2D, CardinalDirection
from .logic import CruciblePath, CityMap, Crucible


def test_initial_crucible_starts_at_origin_facing_east():
    assert CruciblePath.inital_crucible() == Crucible(
        position=Vector2D(0, 0),
        direction=CardinalDirection.EAST,
        num_steps_in_same_direction=0,
    )


SINGLE_BLOCK_MAP = "1"

LARGE_MAP = """2413432311323
               3215453535623
               3255245654254
               3446585845452
               4546657867536
               1438598798454
               4457876987766
               3637877979653
               4654967986887
               4564679986453
               1224686865563
               2546548887735
               4322674655533"""


NINES_MAP = """111111111111
               999999999991
               999999999991
               999999999991
               999999999991"""


@pytest.mark.parametrize(
    "map_grid, final_x, final_y",
    [
        (SINGLE_BLOCK_MAP, 0, 0),
        (LARGE_MAP, 12, 12),
        (NINES_MAP, 11, 4),
    ],
)
def test_city_map_final_position_is_bottom_right(map_grid, final_x, final_y):
    grid = CharacterGrid(map_grid)
    city_map = CityMap(grid)
    assert city_map.final_position == Vector2D(final_x, final_y)


def test_city_map_returns_heat_loss_by_block():
    grid = CharacterGrid(LARGE_MAP)
    city_map = CityMap(grid)
    assert city_map.heat_loss_at(Vector2D(0, 0)) == 2
    assert city_map.heat_loss_at(Vector2D(5, 6)) == 7


@pytest.mark.parametrize(
    "x, y, within_bounds",
    [
        (0, 0, True),
        (11, 4, True),
        (11, 5, False),
        (12, 4, False),
        (-1, 0, False),
        (0, -1, False),
    ],
)
def test_city_map_checks_if_position_is_within_bounds(x, y, within_bounds):
    city_map = CityMap(CharacterGrid(NINES_MAP))
    assert city_map.is_within_bounds(Vector2D(x, y)) == within_bounds


def _example_path() -> CruciblePath:
    city_map = CityMap(CharacterGrid(LARGE_MAP))
    return CruciblePath(
        city_map, min_steps_same_direction=3, max_steps_same_direction=5
    )


def test_crucible_has_not_arrived_at_final_state_if_not_in_final_position():
    crucible = Crucible(
        position=Vector2D(5, 5),
        direction=CardinalDirection.EAST,
        num_steps_in_same_direction=1,
    )
    crucible_path = _example_path()
    assert not crucible_path.is_final_state(crucible)


@pytest.mark.parametrize("invalid_steps", [2, 6])
def test_crucible_has_not_arrived_at_final_state_if_invalid_number_of_steps(
    invalid_steps,
):
    crucible = Crucible(
        position=Vector2D(12, 12),
        direction=CardinalDirection.WEST,
        num_steps_in_same_direction=invalid_steps,
    )
    crucible_path = _example_path()
    assert not crucible_path.is_final_state(crucible)


@pytest.mark.parametrize("valid_steps", [3, 4, 5])
def test_crucible_arrived_at_final_state_if_in_final_position_and_has_valid_number_of_steps(
    valid_steps,
):
    crucible = Crucible(
        position=Vector2D(12, 12),
        direction=CardinalDirection.SOUTH,
        num_steps_in_same_direction=valid_steps,
    )
    crucible_path = _example_path()
    assert crucible_path.is_final_state(crucible)


def test_if_crucible_has_not_reached_minimum_number_of_steps_in_same_direction_it_must_move_forward():
    crucible = Crucible(
        position=Vector2D(5, 5),
        direction=CardinalDirection.SOUTH,
        num_steps_in_same_direction=2,
    )
    crucible_path = _example_path()
    assert list(crucible_path.neighbors(crucible)) == [
        Crucible(
            position=Vector2D(5, 6),
            direction=CardinalDirection.SOUTH,
            num_steps_in_same_direction=3,
        )
    ]


def test_if_crucible_has_reached_maximum_number_of_steps_in_same_direcion_it_must_turn():
    crucible = Crucible(
        position=Vector2D(5, 5),
        direction=CardinalDirection.SOUTH,
        num_steps_in_same_direction=5,
    )
    crucible_path = _example_path()
    assert list(crucible_path.neighbors(crucible)) == [
        Crucible(
            position=Vector2D(6, 5),
            direction=CardinalDirection.EAST,
            num_steps_in_same_direction=1,
        ),
        Crucible(
            position=Vector2D(4, 5),
            direction=CardinalDirection.WEST,
            num_steps_in_same_direction=1,
        ),
    ]


def test_if_crucible_is_between_min_and_max_number_of_steps_in_same_direcion_it_may_go_forward_or_turn():
    crucible = Crucible(
        position=Vector2D(5, 5),
        direction=CardinalDirection.SOUTH,
        num_steps_in_same_direction=3,
    )
    crucible_path = _example_path()
    assert list(crucible_path.neighbors(crucible)) == [
        Crucible(
            position=Vector2D(5, 6),
            direction=CardinalDirection.SOUTH,
            num_steps_in_same_direction=4,
        ),
        Crucible(
            position=Vector2D(6, 5),
            direction=CardinalDirection.EAST,
            num_steps_in_same_direction=1,
        ),
        Crucible(
            position=Vector2D(4, 5),
            direction=CardinalDirection.WEST,
            num_steps_in_same_direction=1,
        ),
    ]


def test_crucible_may_not_leave_city_map():
    crucible = Crucible(
        position=Vector2D(12, 12),
        direction=CardinalDirection.SOUTH,
        num_steps_in_same_direction=4,
    )
    crucible_path = _example_path()
    assert list(crucible_path.neighbors(crucible)) == [
        Crucible(
            position=Vector2D(11, 12),
            direction=CardinalDirection.WEST,
            num_steps_in_same_direction=1,
        ),
    ]


def test_crucible_loses_heat_equal_to_destination_block_when_it_moves():
    origin = Crucible(
        position=Vector2D(5, 5),
        direction=CardinalDirection.SOUTH,
        num_steps_in_same_direction=3,
    )
    destination = Crucible(
        position=Vector2D(5, 6),
        direction=CardinalDirection.SOUTH,
        num_steps_in_same_direction=4,
    )
    crucible_path = _example_path()
    assert crucible_path.weight(origin, destination) == 7


def test_heuristic_potential_of_city_block_is_its_manhattan_distance_to_destination():
    crucible = Crucible(
        position=Vector2D(5, 6),
        direction=CardinalDirection.SOUTH,
        num_steps_in_same_direction=4,
    )
    crucible_path = _example_path()
    assert crucible_path.heuristic_potential(crucible) == 13


@pytest.mark.parametrize(
    "map_grid, min_steps_same_direction, max_steps_same_direction, heat_loss",
    [
        (SINGLE_BLOCK_MAP, 0, 1, 0),
        (LARGE_MAP, 0, 3, 102),
        (LARGE_MAP, 4, 10, 94),
        (NINES_MAP, 4, 10, 71),
    ],
)
def test_crucible_path_minimizes_heat_loss_from_top_left_to_bottom_right(
    map_grid, min_steps_same_direction, max_steps_same_direction, heat_loss
):
    grid = CharacterGrid(map_grid)
    city_map = CityMap(grid)
    crucible_path = CruciblePath(
        city_map, min_steps_same_direction, max_steps_same_direction
    )
    assert crucible_path.min_heat_loss() == heat_loss
