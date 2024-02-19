from collections import defaultdict
from models.vectors import Vector2D
from models.number_theory import gcd


class AsteroidBelt:
    def __init__(self, asteroids: set[Vector2D]):
        self._asteroids = asteroids

    def is_visible(self, asteroid_a, asteroid_b):
        if asteroid_a == asteroid_b:
            return False
        dx = asteroid_b.x - asteroid_a.x
        dy = asteroid_b.y - asteroid_a.y
        num_steps = gcd(abs(dx), abs(dy))
        step = Vector2D(dx // num_steps, dy // num_steps)
        for i in range(1, num_steps):
            if asteroid_a + step * i in self._asteroids:
                return False
        return True

    def asteroid_with_most_visibility(self) -> tuple[Vector2D, int]:
        visibility: dict[Vector2D, set[Vector2D]] = defaultdict(set)
        for asteroid_a in self._asteroids:
            for asteroid_b in self._asteroids:
                if self.is_visible(asteroid_a, asteroid_b):
                    visibility[asteroid_a].add(asteroid_b)
                    visibility[asteroid_b].add(asteroid_a)
        best_location = max(visibility, key=lambda k: len(visibility[k]))
        return best_location, len(visibility[best_location])
