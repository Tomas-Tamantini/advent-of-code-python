from dataclasses import dataclass
from typing import Iterator
import numpy as np


@dataclass(frozen=True)
class LightGridRegion:
    start: tuple[int, int]
    end: tuple[int, int]


class LightGrid:
    def __init__(self, width: int, height: int):
        self._brightness = np.zeros((width, height), dtype=int)

    @property
    def num_lights_on(self) -> int:
        return np.sum(self._brightness > 0)

    @property
    def total_brightness(self) -> int:
        return np.sum(self._brightness)

    def _light_matrix(self, region: LightGridRegion) -> np.ndarray:
        return self._brightness[
            region.start[0] : region.end[0] + 1, region.start[1] : region.end[1] + 1
        ]

    def turn_on(self, region: LightGridRegion) -> None:
        self._light_matrix(region)[:] = 1

    def turn_off(self, region: LightGridRegion) -> None:
        self._light_matrix(region)[:] = 0

    def toggle(self, region: LightGridRegion) -> None:
        self._light_matrix(region)[:] = 1 - self._light_matrix(region)[:]

    def increase_brightness(self, region: LightGridRegion, increase: int) -> None:
        self._light_matrix(region)[:] += increase

    def decrease_brightness(self, region: LightGridRegion, decrease: int) -> None:
        self._light_matrix(region)[:] -= decrease
        self._brightness[self._brightness < 0] = 0
