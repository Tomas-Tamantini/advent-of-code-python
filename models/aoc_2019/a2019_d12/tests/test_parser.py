from models.common.io import InputFromString
from models.common.vectors import Vector3D

from ..parser import parse_3d_vectors


def test_parse_3d_vectors():
    input_reader = InputFromString(" <x=-9, y=10, z=-1>")
    assert list(parse_3d_vectors(input_reader)) == [Vector3D(-9, 10, -1)]
