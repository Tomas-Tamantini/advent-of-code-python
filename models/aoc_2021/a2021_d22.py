from dataclasses import dataclass
from typing import Iterator
from models.vectors import Vector3D


@dataclass(frozen=True)
class Cuboid:
    range_start: Vector3D
    range_end: Vector3D

    def cells_within(self) -> Iterator[Vector3D]:
        for x in range(self.range_start.x, self.range_end.x + 1):
            for y in range(self.range_start.y, self.range_end.y + 1):
                for z in range(self.range_start.z, self.range_end.z + 1):
                    yield Vector3D(x, y, z)

    def all_coords_between(self, min_val: int, max_val: int) -> bool:
        return all(
            min_val <= coord <= max_val
            for coord in (
                self.range_start.x,
                self.range_start.y,
                self.range_start.z,
                self.range_end.x,
                self.range_end.y,
                self.range_end.z,
            )
        )


@dataclass(frozen=True)
class CuboidInstruction:
    cuboid: Cuboid
    turn_on: bool
