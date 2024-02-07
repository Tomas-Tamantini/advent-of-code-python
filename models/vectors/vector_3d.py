from dataclasses import dataclass


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
