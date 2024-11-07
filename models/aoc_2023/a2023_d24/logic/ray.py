from dataclasses import dataclass
from models.common.vectors import Vector2D


@dataclass(frozen=True)
class Ray:
    start: Vector2D
    direction: Vector2D

    def position_at(self, time: float) -> Vector2D:
        return self.start + time * self.direction

    @staticmethod
    def _are_parallel(vector_a: Vector2D, vector_b: Vector2D) -> bool:
        return vector_a.x * vector_b.y == vector_b.x * vector_a.y

    def is_coincident(self, other: "Ray") -> bool:
        delta = self.start - other.start
        return self._are_parallel(
            self.direction, other.direction
        ) and self._are_parallel(self.direction, delta)
