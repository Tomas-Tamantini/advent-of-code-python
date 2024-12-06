from collections import defaultdict
from math import atan2, pi
from typing import Iterator

from models.common.number_theory import gcd
from models.common.vectors import Vector2D


class AsteroidBelt:
    def __init__(self, asteroids: set[Vector2D]):
        self._asteroids = asteroids

    def asteroids_between(self, asteroid_a, asteroid_b) -> Iterator[Vector2D]:
        dx = asteroid_b.x - asteroid_a.x
        dy = asteroid_b.y - asteroid_a.y
        num_steps = gcd(abs(dx), abs(dy))
        step = Vector2D(dx // num_steps, dy // num_steps)
        for i in range(1, num_steps):
            pos = asteroid_a + step * i
            if pos in self._asteroids:
                yield pos

    def is_visible(self, asteroid_a, asteroid_b):
        if asteroid_a == asteroid_b:
            return False
        return not any(
            asteroid in self._asteroids
            for asteroid in self.asteroids_between(asteroid_a, asteroid_b)
        )

    def asteroid_with_most_visibility(self) -> tuple[Vector2D, int]:
        visibility: dict[Vector2D, set[Vector2D]] = defaultdict(set)
        for asteroid_a in self._asteroids:
            for asteroid_b in self._asteroids:
                if self.is_visible(asteroid_a, asteroid_b):
                    visibility[asteroid_a].add(asteroid_b)
                    visibility[asteroid_b].add(asteroid_a)
        best_location = max(visibility, key=lambda k: len(visibility[k]))
        return best_location, len(visibility[best_location])

    def vaporize_asteroids_from(self, gun_location: Vector2D) -> Iterator[Vector2D]:
        sorting_key = dict()
        for asteroid in self._asteroids:
            if asteroid == gun_location:
                continue
            num_asteroids_between = len(
                list(self.asteroids_between(gun_location, asteroid))
            )
            dx = asteroid.x - gun_location.x
            dy = asteroid.y - gun_location.y
            angle = atan2(dx, -dy)
            if angle < 0:
                angle += 2 * pi
            sorting_key[asteroid] = num_asteroids_between, angle
        yield from sorted(sorting_key, key=sorting_key.get)
