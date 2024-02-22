from typing import Iterator
from models.vectors import Vector2D
from .intcode import IntcodeProgram, run_intcode_program


class ScaffoldMap:
    def __init__(self) -> None:
        self._map = ""

    def add_pixel(self, pixel: str) -> None:
        self._map += pixel

    def render(self) -> str:
        return self._map

    def _pixels(self) -> list[list[chr]]:
        return [list(line) for line in self._map.split("\n")]

    def _is_scaffold(self, pixels: list[list[chr]], pos: Vector2D) -> bool:
        if (
            pos.x < 0
            or pos.y < 0
            or pos.y >= len(pixels)
            or pos.x >= len(pixels[pos.y])
        ):
            return False
        return pixels[pos.y][pos.x] in "#^v<>"

    def _is_intersection(self, pixels: list[list[chr]], position: Vector2D) -> bool:
        if not self._is_scaffold(pixels, position):
            return False
        scaffold_neighbors = [
            neighbor
            for neighbor in position.adjacent_positions()
            if self._is_scaffold(pixels, neighbor)
        ]

        return len(scaffold_neighbors) > 2

    def scaffolding_intersections(self) -> Iterator[Vector2D]:
        pixels = self._pixels()
        for y, line in enumerate(pixels):
            for x, _ in enumerate(line):
                position = Vector2D(x, y)
                if self._is_intersection(pixels, position):
                    yield position


class CameraOutput:
    def __init__(self, scaffold_map: ScaffoldMap) -> None:
        self._scaffold_map = scaffold_map

    def write(self, value: int) -> None:
        self._scaffold_map.add_pixel(chr(value))


def run_scaffolding_program(scaffold_map: ScaffoldMap, instructions: list[int]) -> None:
    program = IntcodeProgram(instructions[:])
    camera_output = CameraOutput(scaffold_map)
    run_intcode_program(program, serial_output=camera_output)
