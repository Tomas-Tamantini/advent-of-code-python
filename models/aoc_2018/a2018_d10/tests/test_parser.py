from models.common.io import InputFromString
from models.common.vectors import Vector2D

from ..moving_particles import MovingParticle
from ..parser import parse_moving_particles


def test_parse_moving_particles():
    file_content = """position=< 9,  1> velocity=< 0,  2>
                      position=< 7,  0> velocity=<-1,  0>"""

    particles = list(parse_moving_particles(InputFromString(file_content)))
    assert particles == [
        MovingParticle(position=Vector2D(9, 1), velocity=Vector2D(0, 2)),
        MovingParticle(position=Vector2D(7, 0), velocity=Vector2D(-1, 0)),
    ]
