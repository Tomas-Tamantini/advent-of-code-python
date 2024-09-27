from typing import Iterable
from .vector_2d import Vector2D
from models.common.number_theory import gcd


def twice_polygon_area(vertices: Iterable[Vector2D]) -> int:
    # Shoelace formula
    n = len(vertices)
    return abs(
        sum(vertices[i].vector_product_2d(vertices[(i + 1) % n]) for i in range(n))
    )


def _num_grid_points_on_line_segment(a: Vector2D, b: Vector2D) -> int:
    delta = b - a
    return gcd(abs(delta.x), abs(delta.y)) + 1


def _num_grid_points_on_polygon_perimeter(vertices: Iterable[Vector2D]) -> int:
    return sum(
        _num_grid_points_on_line_segment(vertices[i], vertices[(i + 1) % len(vertices)])
        for i in range(len(vertices))
    ) - len(vertices)


def num_grid_points_inside_polygon(vertices: Iterable[Vector2D]) -> int:
    if len(vertices) < 3:
        return 0
    # Pick's theorem
    twice_area = twice_polygon_area(vertices)
    num_boundary_points = _num_grid_points_on_polygon_perimeter(vertices)
    return (twice_area - num_boundary_points + 2) // 2
