from models.common.vectors import Vector2D
from ..logic import Ray


def test_ray_keeps_track_of_position_at_any_time():
    ray = Ray(start=Vector2D(10, 20), direction=Vector2D(2, -3))
    assert Vector2D(16, 11) == ray.position_at(time=3)


def test_rays_are_not_coincident_if_directions_are_not_parallel():
    ray_a = Ray(start=Vector2D(0, 0), direction=Vector2D(1, 2))
    ray_b = Ray(start=Vector2D(0, 0), direction=Vector2D(1, 3))
    assert not ray_a.is_coincident(ray_b)


def test_rays_are_not_coincident_if_paths_never_meet():
    ray_a = Ray(start=Vector2D(0, 0), direction=Vector2D(1, 2))
    ray_b = Ray(start=Vector2D(0, 1), direction=Vector2D(1, 2))
    assert not ray_a.is_coincident(ray_b)


def test_rays_are_not_coincident_if_paths_meet_in_infinite_many_points():
    ray_a = Ray(start=Vector2D(0, 0), direction=Vector2D(2, 4))
    ray_b = Ray(start=Vector2D(222, 444), direction=Vector2D(-3, -6))
    assert ray_a.is_coincident(ray_b)
