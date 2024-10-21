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
