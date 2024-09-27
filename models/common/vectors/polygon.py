from typing import Iterable, Iterator
from .vector_2d import Vector2D
from models.common.number_theory import gcd


class Polygon:
    def __init__(self, vertices: Iterable[Vector2D]) -> None:
        self._vertices = vertices

    @property
    def _num_vertices(self) -> int:
        return len(self._vertices)

    def _edges(self) -> Iterator[tuple[Vector2D, Vector2D]]:
        for i in range(self._num_vertices):
            yield self._vertices[i], self._vertices[(i + 1) % self._num_vertices]

    def twice_area(self) -> int:
        # Shoelace formula
        return abs(sum(a.vector_product_2d(b) for a, b in self._edges()))

    @staticmethod
    def _num_grid_points_on_line_segment(a: Vector2D, b: Vector2D) -> int:
        delta = b - a
        return gcd(abs(delta.x), abs(delta.y)) + 1

    def num_grid_points_on_perimeter(self) -> int:
        if self._num_vertices <= 1:
            return self._num_vertices
        return (
            sum(self._num_grid_points_on_line_segment(a, b) for a, b in self._edges())
            - self._num_vertices
        )

    def num_grid_points_inside(self) -> int:
        if self._num_vertices < 3:
            return 0
        # Pick's theorem
        num_boundary_points = self.num_grid_points_on_perimeter()
        return (self.twice_area() - num_boundary_points + 2) // 2
