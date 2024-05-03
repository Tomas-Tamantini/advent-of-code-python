from typing import Iterator
from models.vectors import Vector2D


class OctopusesFlashes:
    def __init__(
        self, energy_levels: dict[Vector2D:int], flash_threshold: int = 9
    ) -> None:
        self._energy_levels = energy_levels
        self._num_flashes = 0
        self._flash_threshold = flash_threshold

    @property
    def num_flashes(self) -> int:
        return self._num_flashes

    @property
    def energy_levels(self) -> dict[Vector2D:int]:
        return self._energy_levels

    def _neighbors(self, position: Vector2D) -> Iterator[Vector2D]:
        for neighbor in position.adjacent_positions(include_diagonals=True):
            if neighbor in self._energy_levels:
                yield neighbor

    def step(self) -> None:
        flashing_octopuses = set()

        for pos in self._energy_levels:
            self._energy_levels[pos] += 1
            if self._energy_levels[pos] > self._flash_threshold:
                flashing_octopuses.add(pos)

        self._flash(flashing_octopuses)

    def _flash(self, flashing_octopuses: set[Vector2D]) -> None:
        flashed_octopuses = set()
        while flashing_octopuses:
            pos = flashing_octopuses.pop()
            flashed_octopuses.add(pos)
            self._energy_levels[pos] = 0
            self._num_flashes += 1
            for neighbor in self._neighbors(pos):
                if neighbor not in flashed_octopuses:
                    self._energy_levels[neighbor] += 1
                    if self._energy_levels[neighbor] > self._flash_threshold:
                        flashing_octopuses.add(neighbor)

    def multi_step(self, num_steps: int) -> None:
        for _ in range(num_steps):
            self.step()
