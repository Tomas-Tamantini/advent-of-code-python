from models.common.io import InputFromString
from models.common.vectors import Particle2D, Vector2D

from ..parser import parse_security_robots


def test_parse_security_robots():
    file_content = """p=0,4 v=3,-3
                      p=6,3 v=-1,-3"""
    input_reader = InputFromString(file_content)
    robots = list(parse_security_robots(input_reader))
    assert robots == [
        Particle2D(position=Vector2D(0, 4), velocity=Vector2D(3, -3)),
        Particle2D(position=Vector2D(6, 3), velocity=Vector2D(-1, -3)),
    ]
