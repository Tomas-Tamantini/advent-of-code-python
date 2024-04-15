import pytest
from models.vectors import Vector2D
from models.char_grid import CharacterGrid
from models.aoc_2020 import FerrySeat, FerrySeats


def test_empty_seat_in_ferry_without_occupied_neighbors_becomes_occupied():
    current_state = {
        Vector2D(1, 1): FerrySeat.EMPTY,
        Vector2D(0, 0): FerrySeat.FLOOR,
        Vector2D(2, 2): FerrySeat.EMPTY,
        Vector2D(0, 1): FerrySeat.EMPTY,
    }
    seats = FerrySeats(width=3, height=3, initial_configuration=dict())
    next_state = seats.next_state(current_state)
    assert next_state[Vector2D(1, 1)] == FerrySeat.OCCUPIED


@pytest.mark.parametrize("num_neighbors", [1, 2, 3, 4, 5, 6, 7, 8])
def test_empty_seat_in_ferry_with_one_or_more_occupied_neighbors_remains_empty(
    num_neighbors,
):
    seats = FerrySeats(width=3, height=3, initial_configuration=dict())
    center = Vector2D(1, 1)
    current_state = {center: FerrySeat.EMPTY}
    neighbors = center.adjacent_positions(include_diagonals=True)
    for _ in range(num_neighbors):
        current_state[next(neighbors)] = FerrySeat.OCCUPIED
    next_state = seats.next_state(current_state)
    assert next_state[center] == FerrySeat.EMPTY


@pytest.mark.parametrize("num_neighbors", [0, 1, 2, 3])
def test_occupied_seat_with_three_or_less_occupied_neighbors_remains_occupied(
    num_neighbors,
):
    seats = FerrySeats(width=3, height=3, initial_configuration=dict())
    center = Vector2D(1, 1)
    current_state = {center: FerrySeat.OCCUPIED}
    neighbors = center.adjacent_positions(include_diagonals=True)
    for _ in range(num_neighbors):
        current_state[next(neighbors)] = FerrySeat.OCCUPIED
    next_state = seats.next_state(current_state)
    assert next_state[center] == FerrySeat.OCCUPIED


@pytest.mark.parametrize("num_neighbors", [4, 5, 6, 7, 8])
def test_occupied_seat_with_for_or_more_occupied_neighbors_becomes_empty(
    num_neighbors,
):
    seats = FerrySeats(width=3, height=3, initial_configuration=dict())
    center = Vector2D(1, 1)
    current_state = {center: FerrySeat.OCCUPIED}
    neighbors = center.adjacent_positions(include_diagonals=True)
    for _ in range(num_neighbors):
        current_state[next(neighbors)] = FerrySeat.OCCUPIED
    next_state = seats.next_state(current_state)
    assert next_state[center] == FerrySeat.EMPTY


def test_ferry_seats_reach_steady_state():
    state_str = """
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
    grid = CharacterGrid(state_str)
    seats = FerrySeats.from_char_grid(grid)
    final_state = seats.steady_state()
    assert list(final_state.values()).count(FerrySeat.OCCUPIED) == 37
