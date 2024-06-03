from dataclasses import dataclass
from typing import Iterator, Optional, Iterable
from math import prod
from models.common.vectors import Vector3D


@dataclass(frozen=True)
class Cuboid:
    range_start: Vector3D
    range_end: Vector3D

    def volume(self) -> int:
        return prod(self.range_end[i] - self.range_start[i] + 1 for i in range(3))

    def all_coords_are_between(self, min_val: int, max_val: int) -> bool:
        return all(
            min_val <= coord <= max_val
            for coord in (*self.range_start, *self.range_end)
        )

    def intersect(self, other: "Cuboid") -> Optional["Cuboid"]:
        new_min = [max(self.range_start[i], other.range_start[i]) for i in range(3)]
        new_max = [min(self.range_end[i], other.range_end[i]) for i in range(3)]
        if any(new_min[i] > new_max[i] for i in range(3)):
            return None
        return Cuboid(range_start=Vector3D(*new_min), range_end=Vector3D(*new_max))


@dataclass(frozen=True)
class CuboidInstruction:
    cuboid: Cuboid
    is_turn_on: bool


def _intersections(
    cuboid: Cuboid, instructions: Iterable[CuboidInstruction]
) -> Iterator[CuboidInstruction]:
    for instruction in instructions:
        cuboid_intersection = cuboid.intersect(instruction.cuboid)
        if cuboid_intersection:
            yield CuboidInstruction(
                cuboid=cuboid_intersection,
                is_turn_on=instruction.is_turn_on,
            )


def num_reactor_cells_on(instructions: list[CuboidInstruction]) -> int:
    if len(instructions) == 0:
        return 0
    elif len(instructions) == 1:
        return instructions[0].cuboid.volume() if instructions[0].is_turn_on else 0
    else:
        last_instruction = instructions[-1]
        remaining_instructions = instructions[:-1]
        num_on = num_reactor_cells_on(remaining_instructions)
        if last_instruction.is_turn_on:
            num_on += num_reactor_cells_on(instructions=[last_instruction])
        intersections = list(
            _intersections(last_instruction.cuboid, remaining_instructions)
        )
        num_on -= num_reactor_cells_on(intersections)
        return num_on
