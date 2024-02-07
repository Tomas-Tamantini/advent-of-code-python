from dataclasses import dataclass
from typing import Hashable, Optional
from math import sqrt
from models.vectors import Vector3D


@dataclass(frozen=True)
class Particle:
    id: Hashable
    position: Vector3D
    velocity: Vector3D
    acceleration: Vector3D

    @property
    def manhattan_acceleration(self) -> int:
        return self.acceleration.manhattan_size

    @staticmethod
    def _non_negative_integer_linear_roots(b: int, c: int) -> Optional[int]:
        if b == 0 or c % b != 0:
            return None
        root = -c // b
        return root if root >= 0 else None

    @staticmethod
    def _non_negative_integer_quadratic_roots(a: int, b: int, c: int) -> set[int]:
        if a == 0:
            root = Particle._non_negative_integer_linear_roots(b, c)
            return {root} if root is not None else set()
        delta = b * b - 4 * a * c
        if delta < 0:
            return set()
        sqrt_delta = sqrt(delta)
        if not sqrt_delta.is_integer():
            return set()
        roots = set()
        for numerator in (-b + sqrt_delta, -b - sqrt_delta):
            if numerator % (2 * a) != 0:
                continue
            root = numerator // (2 * a)
            if root >= 0:
                roots.add(root)
        return roots

    def collision_time(self, other: "Particle") -> Optional[int]:
        possible_times = None
        for i in range(3):
            d_acc = self.acceleration[i] - other.acceleration[i]
            d_vel = self.velocity[i] - other.velocity[i]
            d_pos = self.position[i] - other.position[i]
            if d_acc == d_vel == d_pos == 0:
                continue
            times = self._non_negative_integer_quadratic_roots(
                a=d_acc, b=d_acc + 2 * d_vel, c=2 * d_pos
            )
            if possible_times is None:
                possible_times = times
            else:
                possible_times &= times
            if not possible_times:
                return
        return min(possible_times)


@dataclass(frozen=True)
class _Collision:
    particle_a: Particle
    particle_b: Particle
    time: int


class ParticleCollider:
    def __init__(self, particles: list[Particle]) -> None:
        self._particles = particles

    def particle_closest_to_origin_long_term(self) -> Particle:
        return min(self._particles, key=lambda p: p.manhattan_acceleration)

    def _sorted_collisions(self) -> list[_Collision]:
        collisions = []
        for i in range(len(self._particles)):
            for j in range(i + 1, len(self._particles)):
                collision_time = self._particles[i].collision_time(self._particles[j])
                if collision_time is not None:
                    collisions.append(
                        _Collision(
                            self._particles[i], self._particles[j], time=collision_time
                        )
                    )
        return sorted(collisions, key=lambda c: c.time)

    def particles_destroyed_in_collisions(self) -> set[Particle]:
        destroyed_particles = set()
        current_time = -1
        destroyed_this_round = set()
        for collision in self._sorted_collisions():
            if collision.time > current_time:
                destroyed_particles |= destroyed_this_round
                destroyed_this_round = set()
                current_time = collision.time
            if {collision.particle_a, collision.particle_b} & destroyed_particles:
                continue
            destroyed_this_round |= {collision.particle_a, collision.particle_b}
        destroyed_particles |= destroyed_this_round
        return destroyed_particles
