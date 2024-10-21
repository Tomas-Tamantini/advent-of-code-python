from dataclasses import dataclass
from models.common.vectors import Vector3D


@dataclass(frozen=True)
class Brick:
    start: Vector3D
    end: Vector3D

    @property
    def min_z_coordinate(self) -> int:
        return min(self.start.z, self.end.z)

    def drop(self, distance_to_drop) -> "Brick":
        offset = Vector3D(0, 0, distance_to_drop)
        return Brick(start=self.start - offset, end=self.end - offset)
