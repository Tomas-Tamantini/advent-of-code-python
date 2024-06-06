from models.common.io import InputFromString
from models.common.vectors import Vector3D
from ..parser import parse_cube_positions


def test_parse_cube_positions():
    input_str = """
                1, 2, 3
                -12, 10, 20"""
    input_reader = InputFromString(input_str)
    assert list(parse_cube_positions(input_reader)) == [
        Vector3D(1, 2, 3),
        Vector3D(-12, 10, 20),
    ]
