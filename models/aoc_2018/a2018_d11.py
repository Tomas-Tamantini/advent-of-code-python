from math import inf
from dataclasses import dataclass
from typing import Optional
import numpy as np
from models.progress_bar_protocol import ProgressBar


@dataclass(frozen=True)
class _SquareRegion:
    coords_top_left: tuple[int, int]
    size: int


class FuelCells:
    def __init__(self, width: int, height: int, grid_serial_number: int):
        self._width = width
        self._height = height
        self._grid_serial_number = grid_serial_number
        self._grid = self._build_grid()
        self._summed_area_table = self._build_summed_area_table()

    def _build_grid(self):
        grid = np.zeros((self._width, self._height))
        for x in range(self._width):
            for y in range(self._height):
                grid[x, y] = self._calculate_power_level(x, y)
        return grid

    def _calculate_power_level(self, x: int, y: int) -> int:
        rack_id = x + 11
        power_level = rack_id * (y + 1)
        power_level += self._grid_serial_number
        power_level *= rack_id
        power_level = (power_level // 100) % 10
        power_level -= 5
        return power_level

    def power_at(self, x: int, y: int) -> int:
        return self._grid[x, y]

    def _build_summed_area_table(self):
        summed_area_table = np.zeros((self._width, self._height))
        for x in range(self._width):
            for y in range(self._height):
                s = self._grid[x, y]
                if x > 0:
                    s += summed_area_table[x - 1, y]
                if y > 0:
                    s += summed_area_table[x, y - 1]
                if x > 0 and y > 0:
                    s -= summed_area_table[x - 1, y - 1]
                summed_area_table[x, y] = s
        return summed_area_table

    def position_with_largest_total_power(
        self, region_width: int, region_height: int
    ) -> tuple[int, int]:
        max_total_power = -inf
        max_position = None
        for x in range(self._width):
            for y in range(self._height):
                total_power = self._total_power_in_region(
                    x, y, region_width, region_height
                )
                if total_power > max_total_power:
                    max_total_power = total_power
                    max_position = (x, y)
        return max_position

    def square_with_largest_total_power(
        self, progress_bar: Optional[ProgressBar] = None
    ) -> _SquareRegion:
        max_power = -inf
        optimal_square = None
        for size in range(1, min(self._width, self._height) + 1):
            if progress_bar is not None:
                progress_bar.update(size, self._width)
            position = self.position_with_largest_total_power(size, size)
            total_power = self._total_power_in_region(
                position[0], position[1], size, size
            )
            if total_power > max_power:
                max_power = total_power
                optimal_square = _SquareRegion(position, size)

        return optimal_square

    def _total_power_in_region(
        self, x: int, y: int, region_width: int, region_height: int
    ) -> int:
        x_min = x
        x_max = min(x + region_width, self._width) - 1
        y_min = y
        y_max = min(y + region_height, self._height) - 1
        total_power = self._summed_area_table[x_max, y_max]
        if x_min > 0:
            total_power -= self._summed_area_table[x_min - 1, y_max]
        if y_min > 0:
            total_power -= self._summed_area_table[x_max, y_min - 1]
        if x_min > 0 and y_min > 0:
            total_power += self._summed_area_table[x_min - 1, y_min - 1]
        return total_power
