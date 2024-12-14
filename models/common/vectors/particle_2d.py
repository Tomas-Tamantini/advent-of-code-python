from dataclasses import dataclass

from models.common.vectors.vector_2d import Vector2D


@dataclass(frozen=True)
class Particle2D:
    position: Vector2D
    velocity: Vector2D

    def position_at_time(self, time: int) -> Vector2D:
        return self.position + self.velocity * time
