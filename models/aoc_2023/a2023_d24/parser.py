from typing import Iterator

from models.common.io import InputReader
from models.common.vectors import Vector3D

from .logic import Hailstone


def _parse_vector_3d(coord_str: str) -> Vector3D:
    return Vector3D(*map(int, coord_str.split(",")))


def _parse_hailstone(line: str) -> Hailstone:
    parts = line.split("@")
    return Hailstone(
        position=_parse_vector_3d(parts[0]), velocity=_parse_vector_3d(parts[1])
    )


def parse_hailstones(input_reader: InputReader) -> Iterator[Hailstone]:
    for line in input_reader.read_stripped_lines():
        yield _parse_hailstone(line)
