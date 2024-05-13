from dataclasses import dataclass
from typing import Iterator, Optional, Iterable
from models.vectors import Vector3D


@dataclass(frozen=True)
class Cuboid:
    range_start: Vector3D
    range_end: Vector3D

    def volume(self) -> int:
        return (
            (self.range_end.x - self.range_start.x + 1)
            * (self.range_end.y - self.range_start.y + 1)
            * (self.range_end.z - self.range_start.z + 1)
        )

    def all_coords_are_between(self, min_val: int, max_val: int) -> bool:
        return all(
            min_val <= coord <= max_val
            for coord in (
                self.range_start.x,
                self.range_start.y,
                self.range_start.z,
                self.range_end.x,
                self.range_end.y,
                self.range_end.z,
            )
        )

    def intersect(self, other: "Cuboid") -> Optional["Cuboid"]:
        new_min_x = max(self.range_start.x, other.range_start.x)
        new_max_x = min(self.range_end.x, other.range_end.x)
        if new_min_x > new_max_x:
            return None
        new_min_y = max(self.range_start.y, other.range_start.y)
        new_max_y = min(self.range_end.y, other.range_end.y)
        if new_min_y > new_max_y:
            return None
        new_min_z = max(self.range_start.z, other.range_start.z)
        new_max_z = min(self.range_end.z, other.range_end.z)
        if new_min_z > new_max_z:
            return None
        return Cuboid(
            range_start=Vector3D(new_min_x, new_min_y, new_min_z),
            range_end=Vector3D(new_max_x, new_max_y, new_max_z),
        )


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
