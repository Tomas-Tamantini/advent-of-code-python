from typing import Iterator

from models.common.io import InputReader
from models.common.vectors import Vector3D


def _parse_3d_vector(vector_str: str) -> Vector3D:
    coordinates = (
        vector_str.replace("<", "")
        .replace(">", "")
        .replace("=", "")
        .replace("x", "")
        .replace("y", "")
        .replace("z", "")
        .split(",")
    )
    return Vector3D(*map(int, coordinates))


def parse_3d_vectors(input_reader: InputReader) -> Iterator[Vector3D]:
    return map(_parse_3d_vector, input_reader.read_stripped_lines())
