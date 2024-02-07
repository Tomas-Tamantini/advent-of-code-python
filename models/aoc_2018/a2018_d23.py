from dataclasses import dataclass
from models.vectors import Vector3D


@dataclass(frozen=True)
class TeleportNanobot:
    radius: int
    position: Vector3D

    def is_in_range(self, other_position: Vector3D) -> bool:
        return self.position.manhattan_distance(other_position) <= self.radius
