from models.common.vectors import Vector2D, Vector3D

from ..logic import Brick


def test_brick_has_minimum_z_coordinate():
    brick = Brick(start=Vector3D(0, 0, 9), end=Vector3D(0, 0, 5))
    assert brick.min_z_coordinate == 5


def test_brick_has_maximum_z_coordinate():
    brick = Brick(start=Vector3D(0, 0, 9), end=Vector3D(0, 0, 5))
    assert brick.max_z_coordinate == 9


def test_dropping_brick_decrements_its_z_coordinate():
    brick = Brick(start=Vector3D(0, 0, 9), end=Vector3D(0, 0, 5))
    dropped_brick = brick.drop(distance_to_drop=3)
    assert dropped_brick == Brick(start=Vector3D(0, 0, 6), end=Vector3D(0, 0, 2))


def test_brick_iterates_through_xy_projection():
    brick = Brick(start=Vector3D(2, 5, 5), end=Vector3D(2, 3, 5))
    assert set(brick.xy_projection()) == {
        Vector2D(2, 3),
        Vector2D(2, 4),
        Vector2D(2, 5),
    }


def test_brick_checks_whether_it_sits_on_top_of_another():
    brick_a = Brick(start=Vector3D(0, 0, 0), end=Vector3D(3, 0, 0))
    brick_b = Brick(start=Vector3D(3, 0, 1), end=Vector3D(5, 0, 1))
    brick_c = Brick(start=Vector3D(3, 0, 2), end=Vector3D(3, 0, 4))
    brick_d = Brick(start=Vector3D(3, 1, 5), end=Vector3D(3, 1, 5))
    assert brick_b.sits_on_top(brick_a)
    assert brick_c.sits_on_top(brick_b)
    assert not brick_c.sits_on_top(brick_a)
    assert not brick_d.sits_on_top(brick_c)
