from models.common.io import InputFromString
from models.common.vectors import Vector3D
from ..nanobot import TeleportNanobot
from ..parser import parse_nanobots


def test_parse_nanobots():
    file_content = """pos=<1,2,3>, r=4
                      pos=<50,-60,70>, r=81"""
    nanobots = list(parse_nanobots(InputFromString(file_content)))
    assert nanobots == [
        TeleportNanobot(position=Vector3D(1, 2, 3), radius=4),
        TeleportNanobot(position=Vector3D(50, -60, 70), radius=81),
    ]
