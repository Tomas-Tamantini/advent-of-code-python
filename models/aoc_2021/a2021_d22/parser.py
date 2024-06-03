from typing import Iterator
from models.common.io import InputReader
from models.common.vectors import Vector3D
from .reactor_cells import Cuboid, CuboidInstruction


def _parse_cuboid_instruction(line: str) -> CuboidInstruction:
    parts = (
        line.replace("x", "")
        .replace("y", "")
        .replace("z", "")
        .replace(",", "")
        .replace("on", "")
        .replace("off", "")
        .split("=")
    )
    x_min, x_max = map(int, parts[1].split(".."))
    y_min, y_max = map(int, parts[2].split(".."))
    z_min, z_max = map(int, parts[3].split(".."))
    return CuboidInstruction(
        is_turn_on="on" in line,
        cuboid=Cuboid(
            range_start=Vector3D(x_min, y_min, z_min),
            range_end=Vector3D(x_max, y_max, z_max),
        ),
    )


def parse_cuboid_instructions(input_reader: InputReader) -> Iterator[CuboidInstruction]:
    for line in input_reader.read_stripped_lines():
        yield _parse_cuboid_instruction(line)
