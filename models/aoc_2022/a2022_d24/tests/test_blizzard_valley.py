from models.common.vectors import Vector2D, CardinalDirection
from ..logic import BlizzardValley, Blizzard


def test_blizzard_valley_has_walls_around():
    valley = BlizzardValley(
        height=3,
        width=4,
        entrance=Vector2D(1, 0),
        exit=Vector2D(2, 2),
        blizzards=set(),
    )
    assert not valley.is_wall(Vector2D(1, 1))
    assert valley.is_wall(Vector2D(0, 1))
    assert valley.is_wall(Vector2D(3, 1))
    assert valley.is_wall(Vector2D(2, 0))
    assert valley.is_wall(Vector2D(1, 2))


def test_blizzard_valley_has_gap_in_wall_at_entrance_and_exit():
    valley = BlizzardValley(
        height=3,
        width=4,
        entrance=Vector2D(1, 0),
        exit=Vector2D(2, 2),
        blizzards=set(),
    )
    assert not valley.is_wall(Vector2D(1, 0))
    assert not valley.is_wall(Vector2D(2, 2))


def test_position_is_not_free_at_blizzard_valley_if_wall():
    valley = BlizzardValley(
        height=3,
        width=4,
        entrance=Vector2D(1, 0),
        exit=Vector2D(2, 2),
        blizzards=set(),
    )
    assert not valley.position_is_free_at_time(position=Vector2D(0, 0), time=0)
    assert valley.position_is_free_at_time(position=Vector2D(1, 0), time=0)


def test_position_is_not_free_at_blizzard_valley_if_blizzard_is_there_at_that_time():
    blizzard = Blizzard(
        initial_position=Vector2D(1, 1),
        direction=CardinalDirection.EAST,
    )
    valley = BlizzardValley(
        height=3,
        width=4,
        entrance=Vector2D(1, 0),
        exit=Vector2D(2, 2),
        blizzards={blizzard},
    )
    assert not valley.position_is_free_at_time(position=Vector2D(1, 1), time=0)
    assert valley.position_is_free_at_time(position=Vector2D(1, 1), time=1)


def test_blizzard_wraps_around_valley_like_pacman():
    blizzard = Blizzard(
        initial_position=Vector2D(1, 1),
        direction=CardinalDirection.EAST,
    )
    valley = BlizzardValley(
        height=3,
        width=4,
        entrance=Vector2D(1, 0),
        exit=Vector2D(2, 2),
        blizzards={blizzard},
    )
    assert not valley.position_is_free_at_time(position=Vector2D(1, 1), time=1000)
    assert valley.position_is_free_at_time(position=Vector2D(1, 1), time=1001)
