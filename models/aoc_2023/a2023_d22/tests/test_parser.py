from models.common.io import InputFromString
from models.common.vectors import Vector3D

from ..logic import Brick
from ..parser import parse_bricks


def test_parse_bricks_snapshot():
    file_content = """1,3,231~3,3,231
                      4,5,264~4,5,265"""
    input_reader = InputFromString(file_content)
    bricks = list(parse_bricks(input_reader))
    assert bricks == [
        Brick(start=Vector3D(1, 3, 231), end=Vector3D(3, 3, 231)),
        Brick(start=Vector3D(4, 5, 264), end=Vector3D(4, 5, 265)),
    ]
