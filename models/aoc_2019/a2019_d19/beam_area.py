from typing import Iterator, Optional
from math import floor
from dataclasses import dataclass
from models.common.vectors import Vector2D, CardinalDirection
from models.aoc_2019.intcode import IntcodeProgram, run_intcode_program


@dataclass(frozen=True)
class _Square:
    bottom_left: Vector2D
    side_length: int

    @property
    def top_left(self) -> Vector2D:
        return self.bottom_left.move(CardinalDirection.NORTH, self.side_length - 1)

    @property
    def bottom_right(self) -> Vector2D:
        return self.bottom_left.move(CardinalDirection.EAST, self.side_length - 1)

    def move(self, direction: CardinalDirection) -> "_Square":
        return _Square(self.bottom_left.move(direction), self.side_length)

    def bring_closer_to_origin(self, multiplicative_factor: float) -> "_Square":
        new_position = Vector2D(
            floor(self.bottom_left.x * multiplicative_factor),
            floor(self.bottom_left.y * multiplicative_factor),
        )
        return _Square(new_position, self.side_length)


class BeamArea:
    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._points_attracted_to_beam = set()

    def coordinates(self) -> Iterator[Vector2D]:
        for y in range(self._height):
            for x in range(self._width):
                yield Vector2D(x, y)

    def set_point_attracted_to_beam(self, coordinates: Vector2D) -> None:
        self._points_attracted_to_beam.add(coordinates)

    @property
    def num_points_attracted_to_beam(self) -> int:
        return len(self._points_attracted_to_beam)

    def _linear_approximation_coefficients(self) -> tuple[float, float]:
        a_coeff, b_coeff = None, None
        for y in reversed(range(self._height)):
            x_attracted_to_beam = [
                x
                for x in range(self._width)
                if Vector2D(x, y) in self._points_attracted_to_beam
            ]
            if not x_attracted_to_beam:
                continue
            min_x, max_x = min(x_attracted_to_beam), max(x_attracted_to_beam)
            if b_coeff is None:
                b_coeff = y / min_x
            if max_x < self._width - 1:
                a_coeff = y / max_x
                return a_coeff, b_coeff

    def initial_guess_for_square_position(self, side_length: int) -> _Square:
        a, b = self._linear_approximation_coefficients()
        x = floor((side_length - 1) * (1 + a) / (b - a))
        y = floor((side_length - 1) * a * (1 + b) / (b - a))
        return _Square(Vector2D(x, y), side_length)


class _BeamScannerInput:
    def __init__(self, coordinates: Vector2D) -> None:
        self._coordinates = coordinates
        self._current_idx = 0

    def read(self) -> int:
        value = self._coordinates.x if self._current_idx == 0 else self._coordinates.y
        self._current_idx += 1
        return value


class _BeamScannerOutput:
    def __init__(self) -> None:
        self._value = None

    def write(self, value: int) -> None:
        self._value = value

    @property
    def value(self) -> int:
        return self._value


def _run_scammer_for_coordinates(instructions: list[int], coordinates: Vector2D) -> int:
    program = IntcodeProgram(instructions[:])
    scanner_input = _BeamScannerInput(coordinates)
    scanner_output = _BeamScannerOutput()
    run_intcode_program(
        program, serial_input=scanner_input, serial_output=scanner_output
    )
    return scanner_output.value


def run_beam_scanner(instructions: list[int], beam_area: BeamArea) -> None:
    for coordinates in beam_area.coordinates():
        output = _run_scammer_for_coordinates(instructions, coordinates)
        if output == 1:
            beam_area.set_point_attracted_to_beam(coordinates)


def _next_guess_for_closest_square(
    current_guess: _Square, instructions: list[int]
) -> Optional[_Square]:
    top_left_is_inside_beam = _run_scammer_for_coordinates(
        instructions, current_guess.top_left
    )
    if not top_left_is_inside_beam:
        return current_guess.move(CardinalDirection.EAST)

    bottom_right_is_inside_beam = _run_scammer_for_coordinates(
        instructions, current_guess.bottom_right
    )
    if not bottom_right_is_inside_beam:
        return current_guess.move(CardinalDirection.NORTH)

    candidate = current_guess.move(CardinalDirection.WEST)
    top_left_is_inside_beam = _run_scammer_for_coordinates(
        instructions, candidate.top_left
    )
    if top_left_is_inside_beam:
        return candidate

    candidate = current_guess.move(CardinalDirection.SOUTH)
    bottom_right_is_inside_beam = _run_scammer_for_coordinates(
        instructions, candidate.bottom_right
    )
    if bottom_right_is_inside_beam:
        return candidate

    candidate = current_guess.move(CardinalDirection.WEST).move(CardinalDirection.SOUTH)
    top_left_is_inside_beam = _run_scammer_for_coordinates(
        instructions, candidate.top_left
    )
    bottom_right_is_inside_beam = _run_scammer_for_coordinates(
        instructions, candidate.bottom_right
    )
    if top_left_is_inside_beam and bottom_right_is_inside_beam:
        return candidate


def square_closest_to_beam_source(
    side_length: int, instructions: list[int], scanned_area: BeamArea
) -> Vector2D:
    guess = scanned_area.initial_guess_for_square_position(side_length)
    guess = guess.bring_closer_to_origin(0.9)
    while True:
        next_guess = _next_guess_for_closest_square(guess, instructions)
        if next_guess:
            guess = next_guess
        else:
            return guess.bottom_left
