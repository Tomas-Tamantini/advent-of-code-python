from dataclasses import dataclass
from models.common.vectors import Vector3D, Vector2D
from .ray import Ray


@dataclass(frozen=True)
class Hailstone:
    position: Vector3D
    velocity: Vector3D

    def xy_plane_projection(self) -> Ray:
        return Ray(
            start=Vector2D(self.position.x, self.position.y),
            direction=Vector2D(self.velocity.x, self.velocity.y),
        )
