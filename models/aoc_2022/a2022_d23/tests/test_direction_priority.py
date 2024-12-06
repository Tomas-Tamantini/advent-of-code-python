from models.common.vectors import CardinalDirection

from ..logic import direction_priority


def test_direction_priority_of_first_round_is_one_given():
    priority_first_round = [CardinalDirection.NORTH, CardinalDirection.EAST]
    assert direction_priority(priority_first_round, round=0) == priority_first_round


def test_direction_priority_of_second_round_is_rotated_by_one():
    priority_first_round = [
        CardinalDirection.NORTH,
        CardinalDirection.EAST,
        CardinalDirection.SOUTH,
    ]
    assert direction_priority(priority_first_round, round=1) == [
        CardinalDirection.EAST,
        CardinalDirection.SOUTH,
        CardinalDirection.NORTH,
    ]


def test_direction_priority_of_nth_is_rotated_by_n_minus_one():
    priority_first_round = [
        CardinalDirection.NORTH,
        CardinalDirection.EAST,
        CardinalDirection.SOUTH,
        CardinalDirection.WEST,
    ]
    assert direction_priority(priority_first_round, round=40_000_003) == [
        CardinalDirection.WEST,
        CardinalDirection.NORTH,
        CardinalDirection.EAST,
        CardinalDirection.SOUTH,
    ]
