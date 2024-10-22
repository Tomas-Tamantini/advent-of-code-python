from dataclasses import dataclass
from typing import Iterator
from models.common.vectors import Vector3D, Vector2D


@dataclass(frozen=True)
class Brick:
    start: Vector3D
    end: Vector3D

    @property
    def min_z_coordinate(self) -> int:
        return min(self.start.z, self.end.z)

    @property
    def max_z_coordinate(self) -> int:
        return max(self.start.z, self.end.z)

    def drop(self, distance_to_drop) -> "Brick":
        offset = Vector3D(0, 0, distance_to_drop)
        return Brick(start=self.start - offset, end=self.end - offset)

    def xy_projection(self) -> Iterator[Vector2D]:
        diff = self.end - self.start
        size = diff.manhattan_size
        first_cell = Vector2D(self.start.x, self.start.y)
        if diff.z != 0 or size == 0:
            yield first_cell
        else:
            offset = Vector2D(diff.x // size, diff.y // size)
            for i in range(size + 1):
                yield first_cell + i * offset

    def sits_on_top(self, base_brick: "Brick") -> bool:
        if self.min_z_coordinate != base_brick.max_z_coordinate + 1:
            return False
        base_coords = set(base_brick.xy_projection())
        top_coords = set(self.xy_projection())
        return len(base_coords.intersection(top_coords)) > 0
