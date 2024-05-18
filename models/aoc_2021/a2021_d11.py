from typing import Iterator
from models.common.vectors import Vector2D, BoundingBox


class OctopusesFlashes:
    def __init__(
        self, energy_levels: dict[Vector2D:int], flash_threshold: int = 9
    ) -> None:
        self._energy_levels = energy_levels
        self._num_flashes = 0
        self._flash_threshold = flash_threshold
        self._all_octopuses_flashed_last_step = False

    @property
    def num_flashes(self) -> int:
        return self._num_flashes

    @property
    def energy_levels(self) -> dict[Vector2D:int]:
        return self._energy_levels

    @property
    def all_octopuses_flashed_last_step(self) -> bool:
        return self._all_octopuses_flashed_last_step

    @property
    def num_octopuses(self) -> int:
        return len(self._energy_levels)

    def _neighbors(self, position: Vector2D) -> Iterator[Vector2D]:
        for neighbor in position.adjacent_positions(include_diagonals=True):
            if neighbor in self._energy_levels:
                yield neighbor

    def step(self) -> None:
        old_num_flashes = self._num_flashes
        flashing_octopuses = set()

        for pos in self._energy_levels:
            self._energy_levels[pos] += 1
            if self._energy_levels[pos] > self._flash_threshold:
                flashing_octopuses.add(pos)

        self._flash(flashing_octopuses)

        num_flashes_this_step = self._num_flashes - old_num_flashes
        self._all_octopuses_flashed_last_step = (
            num_flashes_this_step == self.num_octopuses
        )

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

    def render(self) -> str:
        bounding_box = BoundingBox.from_points(self._energy_levels.keys())
        min_x, max_x = bounding_box.min_x, bounding_box.max_x
        min_y, max_y = bounding_box.min_y, bounding_box.max_y
        rows = []
        for y in range(min_y, max_y + 1):
            current_row = ""
            for x in range(min_x, max_x + 1):
                pos = Vector2D(x, y)
                energy_level = self._energy_levels.get(pos, 0)
                current_row += str(energy_level)
            rows.append(current_row)
        return "\n".join(rows)
