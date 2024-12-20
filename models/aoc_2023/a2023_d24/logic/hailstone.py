from dataclasses import dataclass

from models.common.vectors import Vector2D, Vector3D

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

    def pos_vel_cross_product(self) -> Vector3D:
        return self.position.vector_product(self.velocity)
