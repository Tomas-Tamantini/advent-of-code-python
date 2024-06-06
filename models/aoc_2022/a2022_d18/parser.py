from typing import Iterator
from models.common.vectors import Vector3D
from models.common.io import InputReader


def parse_cube_positions(input_reader: InputReader) -> Iterator[Vector3D]:
    for line in input_reader.read_stripped_lines():
        yield Vector3D(*map(int, line.split(",")))
