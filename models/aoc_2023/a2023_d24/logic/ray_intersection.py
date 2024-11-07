import numpy as np
from models.common.vectors import BoundingBox
from .ray import Ray


def rays_intersect(ray_a: Ray, ray_b: Ray, test_area: BoundingBox) -> bool:
    delta = ray_b.start - ray_a.start
    a = np.array(
        [
            [ray_a.direction.x, -ray_b.direction.x],
            [ray_a.direction.y, -ray_b.direction.y],
        ]
    )
    if np.linalg.det(a) == 0:
        return _parallel_rays_intersect(ray_a, ray_b, test_area)
    else:
        b = np.array([delta.x, delta.y])
        solution = np.linalg.solve(a, b)
        if any(t < 0 for t in solution):
            return False
        intersection = ray_a.position_at(time=solution[0])
        return test_area.contains(intersection)


def _parallel_rays_intersect(ray_a: Ray, ray_b: Ray, test_area: BoundingBox) -> bool:
    if ray_a.is_coincident(ray_b):
        raise NotImplementedError("Logic not implemented for coincident rays")
    else:
        return False
