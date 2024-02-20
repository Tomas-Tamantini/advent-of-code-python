from dataclasses import dataclass
from typing import Iterator
from models.vectors import Vector3D


@dataclass
class MoonOfJupiter:
    position: Vector3D
    velocity: Vector3D = Vector3D()

    @staticmethod
    def _velocity_offset(my_coord: int, other_coord: int) -> int:
        if my_coord < other_coord:
            return 1
        elif my_coord > other_coord:
            return -1
        else:
            return 0

    def apply_gravity(self, other: "MoonOfJupiter") -> None:
        offset = Vector3D(
            *(
                self._velocity_offset(coord_a, coord_b)
                for coord_a, coord_b in zip(self.position, other.position)
            )
        )
        self.velocity = self.velocity + offset
        other.velocity = other.velocity - offset

    def apply_velocity(self) -> None:
        self.position = self.position + self.velocity


class MoonSystem:
    def __init__(self, moons: list[MoonOfJupiter]) -> None:
        self._moons = moons

    @property
    def moons(self) -> list[MoonOfJupiter]:
        return self._moons

    def pairs_of_moons(self) -> Iterator[tuple[MoonOfJupiter, MoonOfJupiter]]:
        for i in range(len(self.moons)):
            for j in range(i + 1, len(self.moons)):
                yield self.moons[i], self.moons[j]

    def step(self) -> None:
        for moon_a, moon_b in self.pairs_of_moons():
            moon_a.apply_gravity(moon_b)
        for moon in self.moons:
            moon.apply_velocity()

    def multi_step(self, num_steps: int) -> None:
        for _ in range(num_steps):
            self.step()
