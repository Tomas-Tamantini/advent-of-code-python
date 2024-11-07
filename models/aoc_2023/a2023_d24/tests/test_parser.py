from models.common.io import InputFromString
from models.common.vectors import Vector3D
from ..logic import Hailstone
from ..parser import parse_hailstones


def test_parse_hailstones():
    file_content = """19, 13, 30 @ -2,  1, -2
                      18, 19, 22 @ -1, -1, -2"""
    input_reader = InputFromString(file_content)
    hailstones = list(parse_hailstones(input_reader))
    assert hailstones == [
        Hailstone(position=Vector3D(19, 13, 30), velocity=Vector3D(-2, 1, -2)),
        Hailstone(position=Vector3D(18, 19, 22), velocity=Vector3D(-1, -1, -2)),
    ]
