from typing import Iterator
from models.aoc_2019.intcode import IntcodeProgram, run_intcode_program


class BeamArea:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._points_attracted_to_beam = set()

    def coordinates(self) -> Iterator[tuple[int, int]]:
        for y in range(self._height):
            for x in range(self._width):
                yield (x, y)

    def set_point_attracted_to_beam(self, x: int, y: int) -> None:
        self._points_attracted_to_beam.add((x, y))

    @property
    def num_points_attracted_to_beam(self) -> int:
        return len(self._points_attracted_to_beam)


class _BeamScannerInput:
    def __init__(self, *coordinates: int) -> None:
        self._coordinates = coordinates
        self._current_idx = 0

    def read(self) -> int:
        value = self._coordinates[self._current_idx]
        self._current_idx += 1
        return value


class _BeamScannerOutput:
    def __init__(self, beam_area: BeamArea, *coordinates: int) -> None:
        self._beam_area = beam_area
        self._coordinates = coordinates

    def write(self, value: int) -> None:
        if value == 1:
            self._beam_area.set_point_attracted_to_beam(*self._coordinates)


def run_beam_scanner(instructions: list[int], beam_area: BeamArea) -> None:
    for coordinates in beam_area.coordinates():
        program = IntcodeProgram(instructions[:])
        scanner_input = _BeamScannerInput(*coordinates)
        scanner_output = _BeamScannerOutput(beam_area, *coordinates)
        run_intcode_program(
            program, serial_input=scanner_input, serial_output=scanner_output
        )
