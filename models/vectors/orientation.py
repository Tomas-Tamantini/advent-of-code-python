from models.vectors import Vector3D
from dataclasses import dataclass


@dataclass(frozen=True)
class Orientation:
    x_prime: Vector3D
    y_prime: Vector3D

    @property
    def z_prime(self) -> Vector3D:
        return self.x_prime.vector_product(self.y_prime)

    def to_absolute_coordinates(self, relative_coordinates: Vector3D) -> Vector3D:
        return (
            relative_coordinates.x * self.x_prime
            + relative_coordinates.y * self.y_prime
            + relative_coordinates.z * self.z_prime
        )

    @classmethod
    def all_orientations_aligned_with_grid_axes(cls):
        grid_axes = (Vector3D(1, 0, 0), Vector3D(0, 1, 0), Vector3D(0, 0, 1))
        for x_prime in grid_axes:
            for y_prime in grid_axes:
                if x_prime != y_prime:
                    yield cls(x_prime, y_prime)
                    yield cls(x_prime, -y_prime)
                    yield cls(-x_prime, y_prime)
                    yield cls(-x_prime, -y_prime)
