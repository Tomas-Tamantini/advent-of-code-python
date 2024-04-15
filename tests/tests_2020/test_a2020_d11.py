import pytest
from models.vectors import Vector2D
from models.aoc_2020 import FerrySeat, FerrySeats


def test_empty_seat_in_ferry_without_occupied_neighbors_becomes_occupied():
    seats = FerrySeats(width=3, height=3)
    current_state = {
        Vector2D(1, 1): FerrySeat.EMPTY,
        Vector2D(0, 0): FerrySeat.FLOOR,
        Vector2D(2, 2): FerrySeat.EMPTY,
        Vector2D(0, 1): FerrySeat.EMPTY,
    }
    next_state = seats.next_state(current_state)
    assert next_state[Vector2D(1, 1)] == FerrySeat.OCCUPIED


@pytest.mark.parametrize("num_neighbors", [1, 2, 3, 4, 5, 6, 7, 8])
def test_empty_seat_in_ferry_with_one_or_more_occupied_neighbors_remains_empty(
    num_neighbors,
):
    seats = FerrySeats(width=3, height=3)
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
    seats = FerrySeats(width=3, height=3)
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
    seats = FerrySeats(width=3, height=3)
    center = Vector2D(1, 1)
    current_state = {center: FerrySeat.OCCUPIED}
    neighbors = center.adjacent_positions(include_diagonals=True)
    for _ in range(num_neighbors):
        current_state[next(neighbors)] = FerrySeat.OCCUPIED
    next_state = seats.next_state(current_state)
    assert next_state[center] == FerrySeat.EMPTY


def _state_from_str(state_str: str) -> tuple[int, int, dict[Vector2D, FerrySeat]]:
    state = state_str.strip().split("\n")
    width = len(state[0].strip())
    height = len(state)
    seats = {}
    for y, row in enumerate(state):
        for x, cell in enumerate(row.strip()):
            seats[Vector2D(x, y)] = FerrySeat(cell)
    return width, height, seats


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
    width, height, initial_state = _state_from_str(state_str)
    seats = FerrySeats(width=width, height=height)
    final_state = seats.steady_state(initial_state)
    assert list(final_state.values()).count(FerrySeat.OCCUPIED) == 37
