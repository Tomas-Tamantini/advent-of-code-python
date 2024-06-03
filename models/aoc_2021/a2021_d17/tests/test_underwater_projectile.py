from models.common.vectors import Vector2D, BoundingBox
from ..underwater_projectile import UnderwaterProjectile


def test_underwater_projectile_starts_at_origin():
    projectile = UnderwaterProjectile()
    new_position = projectile.position_at(step=0, initial_velocity=Vector2D(0, 0))
    assert new_position == Vector2D(0, 0)


def test_underwater_projectile_accelerates_along_y_axis_due_to_gravity():
    projectile = UnderwaterProjectile()
    y_positions = [
        projectile.position_at(step=i, initial_velocity=Vector2D(0, 2)).y
        for i in range(7)
    ]
    assert y_positions == [0, 2, 3, 3, 2, 0, -3]


def test_underwater_projectile_deaccelerates_along_x_axis_due_to_drag():
    projectile = UnderwaterProjectile()
    x_positions = [
        projectile.position_at(step=i, initial_velocity=Vector2D(6, 0)).x
        for i in range(10)
    ]
    assert x_positions == [0, 6, 11, 15, 18, 20, 21, 21, 21, 21]


def test_underwater_projectile_reaches_maximum_height_at_triangular_numbers():
    projectile = UnderwaterProjectile()
    assert projectile.maximum_height(initial_y_velocity=2) == 3
    assert projectile.maximum_height(initial_y_velocity=9) == 45


def test_underwater_projectile_reaches_target_at_specific_velocities():
    target = BoundingBox(
        bottom_left=Vector2D(20, -10),
        top_right=Vector2D(30, -5),
    )
    velocities = list(UnderwaterProjectile.velocities_to_reach_target(target))
    assert len(velocities) == 112
