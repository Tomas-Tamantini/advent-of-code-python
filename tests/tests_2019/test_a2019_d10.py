from models.common.vectors import Vector2D
from models.aoc_2019.a2019_d10 import AsteroidBelt


def test_asteroid_is_not_visible_to_itself():
    asteroid = Vector2D(0, 0)
    asteroid_belt = AsteroidBelt(asteroids={asteroid})
    assert not asteroid_belt.is_visible(asteroid, asteroid)


def test_two_asteroids_are_visible_if_none_between_them():
    asteroid_a = Vector2D(3, 10)
    asteroid_b = Vector2D(9, 1)
    asteroid_belt = AsteroidBelt(asteroids={asteroid_a, asteroid_b})
    assert asteroid_belt.is_visible(asteroid_a, asteroid_b)
    assert asteroid_belt.is_visible(asteroid_b, asteroid_a)


def test_two_asteroids_are_not_visible_if_some_between_them():
    asteroid_a = Vector2D(3, 10)
    asteroid_b = Vector2D(5, 7)
    asteroid_c = Vector2D(9, 1)
    asteroid_belt = AsteroidBelt(asteroids={asteroid_a, asteroid_b, asteroid_c})
    assert not asteroid_belt.is_visible(asteroid_a, asteroid_c)
    assert not asteroid_belt.is_visible(asteroid_c, asteroid_a)

    assert asteroid_belt.is_visible(asteroid_a, asteroid_b)
    assert asteroid_belt.is_visible(asteroid_b, asteroid_a)

    assert asteroid_belt.is_visible(asteroid_b, asteroid_c)
    assert asteroid_belt.is_visible(asteroid_c, asteroid_b)


def test_can_find_asteroid_with_most_visibility():
    asteroid_belt = AsteroidBelt(
        asteroids={
            Vector2D(1, 0),
            Vector2D(4, 0),
            Vector2D(0, 2),
            Vector2D(1, 2),
            Vector2D(2, 2),
            Vector2D(3, 2),
            Vector2D(4, 2),
            Vector2D(4, 3),
            Vector2D(3, 4),
            Vector2D(4, 4),
        }
    )
    best_location, others_visible = asteroid_belt.asteroid_with_most_visibility()
    assert best_location == Vector2D(3, 4)
    assert others_visible == 8


def test_asteroids_are_vaporized_in_clockwise_order_starting_from_north():
    asteroid_belt = AsteroidBelt(
        asteroids={
            Vector2D(0, 0),
            Vector2D(1, 0),
            Vector2D(-1, 0),
            Vector2D(0, 1),
            Vector2D(0, -1),
        }
    )
    asteroids_shot = asteroid_belt.vaporize_asteroids_from(Vector2D(0, 0))
    assert list(asteroids_shot) == [
        Vector2D(0, -1),
        Vector2D(1, 0),
        Vector2D(0, 1),
        Vector2D(-1, 0),
    ]


def test_asteroids_blocked_by_others_have_to_wait_full_rotation_before_being_vaporized():
    asteroid_belt = AsteroidBelt(
        asteroids={
            Vector2D(0, 1),
            Vector2D(0, 2),
            Vector2D(0, 3),
            Vector2D(0, 5),
            Vector2D(1, 0),
            Vector2D(1, 8),
            Vector2D(2, 5),
            Vector2D(2, 11),
        }
    )
    asteroids_shot = asteroid_belt.vaporize_asteroids_from(Vector2D(0, 5))
    assert list(asteroids_shot) == [
        Vector2D(0, 3),
        Vector2D(1, 0),
        Vector2D(2, 5),
        Vector2D(1, 8),
        Vector2D(0, 2),
        Vector2D(2, 11),
        Vector2D(0, 1),
    ]
