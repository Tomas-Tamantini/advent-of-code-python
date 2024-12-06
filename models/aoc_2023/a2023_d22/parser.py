from typing import Iterator

from models.common.io import InputReader
from models.common.vectors import Vector3D

from .logic import Brick


def _parse_brick(line: str) -> Brick:
    parts = line.split("~")
    return Brick(start=Vector3D(*eval(parts[0])), end=Vector3D(*eval(parts[1])))


def parse_bricks(input_reader: InputReader) -> Iterator[Brick]:
    for line in input_reader.read_stripped_lines():
        yield _parse_brick(line)
