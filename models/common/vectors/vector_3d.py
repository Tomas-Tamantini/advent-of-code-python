from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True, order=True)
class Vector3D:
    x: int = 0
    y: int = 0
    z: int = 0

    def manhattan_distance(self, other: "Vector3D") -> int:
        return sum(abs(coord_a - coord_b) for coord_a, coord_b in zip(self, other))

    @property
    def manhattan_size(self) -> int:
        return sum(abs(coord) for coord in self)

    def adjacent_positions(
        self, include_diagonals: bool = True
    ) -> Iterator["Vector3D"]:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    if dx == dy == dz == 0:
                        continue
                    if (
                        not include_diagonals
                        and sum(abs(coord) for coord in (dx, dy, dz)) > 1
                    ):
                        continue
                    yield Vector3D(self.x + dx, self.y + dy, self.z + dz)

    def vector_product(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def __getitem__(self, item):
        if item == 0:
            return self.x
        if item == 1:
            return self.y
        if item == 2:
            return self.z
        raise IndexError

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __add__(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self) -> "Vector3D":
        return Vector3D(-self.x, -self.y, -self.z)

    def __mul__(self, scalar: int) -> "Vector3D":
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: int) -> "Vector3D":
        return self.__mul__(scalar)
