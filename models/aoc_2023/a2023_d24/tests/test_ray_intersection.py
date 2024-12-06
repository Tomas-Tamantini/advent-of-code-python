from models.common.vectors import BoundingBox, Vector2D

from ..logic import Ray, rays_intersect


def test_parallel_rays_do_not_intersect():
    ray_a = Ray(start=Vector2D(0, 0), direction=Vector2D(1, 0))
    ray_b = Ray(start=Vector2D(0, 1), direction=Vector2D(1, 0))
    test_area = BoundingBox(Vector2D(0, 0), Vector2D(27, 27))
    assert not rays_intersect(ray_a, ray_b, test_area)


def test_rays_whose_path_intersection_was_in_the_past_do_not_intersect():
    ray_a = Ray(start=Vector2D(1, 0), direction=Vector2D(0, 1))
    ray_b = Ray(start=Vector2D(0, 1), direction=Vector2D(-1, 0))
    test_area = BoundingBox(Vector2D(0, 0), Vector2D(27, 27))
    assert not rays_intersect(ray_a, ray_b, test_area)


def test_rays_whose_path_intersection_is_outside_test_area_do_not_intersect():
    ray_a = Ray(start=Vector2D(100, 0), direction=Vector2D(0, 1))
    ray_b = Ray(start=Vector2D(0, 100), direction=Vector2D(1, 0))
    test_area = BoundingBox(Vector2D(0, 0), Vector2D(27, 27))
    assert not rays_intersect(ray_a, ray_b, test_area)


def test_rays_whose_path_intersection_is_inside_test_area_intersect():
    ray_a = Ray(start=Vector2D(100, 0), direction=Vector2D(0, 1))
    ray_b = Ray(start=Vector2D(0, 100), direction=Vector2D(1, 0))
    test_area = BoundingBox(Vector2D(99, 99), Vector2D(101, 101))
    assert rays_intersect(ray_a, ray_b, test_area)
