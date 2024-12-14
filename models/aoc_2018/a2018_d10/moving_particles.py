from dataclasses import dataclass
from typing import Iterator

from models.common.vectors import BoundingBox, Particle2D


@dataclass(frozen=True)
class MovingParticles:
    particles: tuple[Particle2D, ...]

    def bounding_box_at_time(self, time: int) -> BoundingBox:
        return BoundingBox.from_points(
            particle.position_at_time(time) for particle in self.particles
        )

    def moments_of_bounding_box_area_increase(self) -> Iterator[int]:
        area_before = self.bounding_box_at_time(0).area
        t = 1
        while True:
            area = self.bounding_box_at_time(t).area
            if area > area_before:
                yield t
            t += 1
            area_before = area

    def draw(self, time: int) -> str:
        bounding_box = self.bounding_box_at_time(time)
        matrix = [
            ["."] * (bounding_box.width + 1) for _ in range(bounding_box.height + 1)
        ]
        for particle in self.particles:
            position = particle.position_at_time(time) - bounding_box.bottom_left
            matrix[position.y][position.x] = "#"
        return "\n".join("".join(row) for row in matrix)
