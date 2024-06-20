from models.common.vectors import Vector2D, CardinalDirection
from ..logic import AntisocialElves


def test_antisocial_elves_without_neighbors_do_not_propose_to_move():
    elves = AntisocialElves(positions={Vector2D(0, 0)})
    elves.move(
        direction_priority=(
            CardinalDirection.EAST,
            CardinalDirection.NORTH,
            CardinalDirection.WEST,
            CardinalDirection.SOUTH,
        )
    )
    assert elves.positions == {Vector2D(0, 0)}


def test_antisocial_elves_with_one_or_more_neighbors_propose_to_move_according_to_direction_priority():
    elves = AntisocialElves(positions={Vector2D(0, 0), Vector2D(1, 0)})
    direction_priority = (
        CardinalDirection.EAST,
        CardinalDirection.NORTH,
        CardinalDirection.WEST,
        CardinalDirection.SOUTH,
    )
    elves.move(direction_priority)
    assert elves.positions == {Vector2D(0, -1), Vector2D(2, 0)}


def test_antisocial_elves_do_not_move_if_more_than_one_proposed_the_same_move():
    elves = AntisocialElves(
        positions={Vector2D(0, 0), Vector2D(0, 1), Vector2D(0, 3), Vector2D(1, 4)}
    )
    direction_priority = (
        CardinalDirection.NORTH,
        CardinalDirection.SOUTH,
        CardinalDirection.WEST,
        CardinalDirection.EAST,
    )
    elves.move(direction_priority)
    assert elves.positions == {
        Vector2D(0, -1),
        Vector2D(0, 1),
        Vector2D(0, 3),
        Vector2D(1, 5),
    }


def test_antisocial_elves_keep_track_of_how_many_elves_moved_last_round():
    elves = AntisocialElves(
        positions={Vector2D(0, 0), Vector2D(0, 1), Vector2D(0, 3), Vector2D(1, 4)}
    )
    direction_priority = (
        CardinalDirection.NORTH,
        CardinalDirection.SOUTH,
        CardinalDirection.WEST,
        CardinalDirection.EAST,
    )
    elves.move(direction_priority)
    assert elves.num_elves_that_moved_last_round == 2
