import pytest

from models.common.io import CharacterGrid
from models.common.vectors import Vector2D

from .ferry_seats import FerrySeat, FerrySeats


def test_empty_seat_in_ferry_without_occupied_neighbors_becomes_occupied():
    initial_configuration = {
        Vector2D(1, 1): FerrySeat.EMPTY,
        Vector2D(0, 0): FerrySeat.FLOOR,
        Vector2D(2, 2): FerrySeat.EMPTY,
        Vector2D(0, 1): FerrySeat.EMPTY,
    }
    seats = FerrySeats(width=3, height=3, initial_configuration=initial_configuration)
    next_state = seats.next_state(initial_configuration)
    assert next_state[Vector2D(1, 1)] == FerrySeat.OCCUPIED


@pytest.mark.parametrize("num_neighbors", [1, 2, 3, 4, 5, 6, 7, 8])
def test_empty_seat_in_ferry_with_one_or_more_occupied_neighbors_remains_empty(
    num_neighbors,
):
    center = Vector2D(1, 1)
    initial_configuration = {center: FerrySeat.EMPTY}
    neighbors = center.adjacent_positions(include_diagonals=True)
    for _ in range(num_neighbors):
        initial_configuration[next(neighbors)] = FerrySeat.OCCUPIED
    seats = FerrySeats(width=3, height=3, initial_configuration=initial_configuration)
    next_state = seats.next_state(initial_configuration)
    assert next_state[center] == FerrySeat.EMPTY


@pytest.mark.parametrize("num_neighbors", [0, 1, 2, 3])
def test_occupied_seat_with_occupied_neighbors_within_tolerance_remains_occupied(
    num_neighbors,
):
    center = Vector2D(1, 1)
    initial_configuration = {center: FerrySeat.OCCUPIED}
    neighbors = center.adjacent_positions(include_diagonals=True)
    for _ in range(num_neighbors):
        initial_configuration[next(neighbors)] = FerrySeat.OCCUPIED
    seats = FerrySeats(
        width=3,
        height=3,
        initial_configuration=initial_configuration,
        occupied_neighbors_tolerance=3,
    )
    next_state = seats.next_state(initial_configuration)
    assert next_state[center] == FerrySeat.OCCUPIED


@pytest.mark.parametrize("num_neighbors", [4, 5, 6, 7, 8])
def test_occupied_seat_with_more_occupied_neighbors_than_tolerated_becomes_empty(
    num_neighbors,
):
    center = Vector2D(1, 1)
    initial_configuration = {center: FerrySeat.OCCUPIED}
    neighbors = center.adjacent_positions(include_diagonals=True)
    for _ in range(num_neighbors):
        initial_configuration[next(neighbors)] = FerrySeat.OCCUPIED
    seats = FerrySeats(
        width=3,
        height=3,
        initial_configuration=initial_configuration,
        occupied_neighbors_tolerance=3,
    )
    next_state = seats.next_state(initial_configuration)
    assert next_state[center] == FerrySeat.EMPTY


def test_ferry_can_consider_neighbors_as_first_chair_in_line_of_site_rather_than_adjacent_floor_cells():
    grid = CharacterGrid(
        """
        #.L..
        .....
        L.#.L
        .....
        ..L.#  
        """
    )
    seats = FerrySeats(
        width=grid.width,
        height=grid.height,
        initial_configuration=grid.tiles,
        consider_only_adjacent_neighbors=False,
    )
    neighbors = list(seats.neighbors(Vector2D(2, 2)))
    assert len(neighbors) == 6
    assert set(neighbors) == {
        Vector2D(0, 0),
        Vector2D(2, 0),
        Vector2D(0, 2),
        Vector2D(4, 2),
        Vector2D(2, 4),
        Vector2D(4, 4),
    }


example_config = """
                 L.LL.LL.LL
                 LLLLLLL.LL
                 L.L.L..L..
                 LLLL.LL.LL
                 L.LL.LL.LL
                 L.LLLLL.LL
                 ..L.L.....
                 LLLLLLLLLL
                 L.LLLLLL.L
                 L.LLLLL.LL
                 """


def test_ferry_seats_reach_steady_state():
    grid = CharacterGrid(example_config)
    seats = FerrySeats(
        width=grid.width,
        height=grid.height,
        initial_configuration=grid.tiles,
        occupied_neighbors_tolerance=3,
        consider_only_adjacent_neighbors=True,
    )
    final_state = seats.steady_state()
    assert list(final_state.values()).count(FerrySeat.OCCUPIED) == 37


def test_ferry_seats_reach_steady_state_with_different_tolerance_levels():
    grid = CharacterGrid(example_config)
    seats = FerrySeats(
        width=grid.width,
        height=grid.height,
        initial_configuration=grid.tiles,
        occupied_neighbors_tolerance=4,
        consider_only_adjacent_neighbors=False,
    )
    final_state = seats.steady_state()
    assert list(final_state.values()).count(FerrySeat.OCCUPIED) == 26
