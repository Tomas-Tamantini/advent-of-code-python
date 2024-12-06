from models.common.vectors import Vector3D

from ..logic import Brick, drop_bricks


def test_brick_on_ground_stays_on_ground():
    brick = Brick(start=Vector3D(10, 10, 10), end=Vector3D(10, 10, 1))
    assert set(drop_bricks({brick})) == {brick}


def test_unobstructed_brick_will_fall_to_ground():
    brick = Brick(start=Vector3D(10, 10, 10), end=Vector3D(10, 10, 5))
    assert set(drop_bricks({brick})) == {
        Brick(start=Vector3D(10, 10, 6), end=Vector3D(10, 10, 1))
    }


def test_bricks_fall_until_resting_on_other_bricks():
    bricks = {
        Brick(start=Vector3D(0, 0, 10), end=Vector3D(0, 0, 5)),
        Brick(start=Vector3D(0, 4, 500), end=Vector3D(0, -1, 500)),
        Brick(start=Vector3D(0, 3, 1000), end=Vector3D(0, 3, 1002)),
    }
    assert set(drop_bricks(bricks)) == {
        Brick(start=Vector3D(0, 0, 6), end=Vector3D(0, 0, 1)),
        Brick(start=Vector3D(0, 4, 7), end=Vector3D(0, -1, 7)),
        Brick(start=Vector3D(0, 3, 8), end=Vector3D(0, 3, 10)),
    }
