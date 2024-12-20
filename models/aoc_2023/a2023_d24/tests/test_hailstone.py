from models.common.vectors import Vector2D, Vector3D

from ..logic import Hailstone, Ray


def test_hailstone_xy_projection_ignores_z_coordinate():
    hailstone = Hailstone(position=Vector3D(1, 2, 3), velocity=Vector3D(10, 20, 30))
    assert hailstone.xy_plane_projection() == Ray(
        start=Vector2D(1, 2), direction=Vector2D(10, 20)
    )


def test_hailstone_calculates_vector_product_between_position_and_velocity():
    hailstone = Hailstone(position=Vector3D(1, 2, 3), velocity=Vector3D(5, 6, 4))
    assert hailstone.pos_vel_cross_product() == Vector3D(-10, 11, -4)
