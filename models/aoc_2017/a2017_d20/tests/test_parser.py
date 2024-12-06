from models.common.io import InputFromString
from models.common.vectors import Vector3D

from ..parser import parse_particles
from ..particle_collider import Particle


def test_parse_particles():
    file_content = """p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
                      p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>"""
    particles = list(parse_particles(InputFromString(file_content)))
    assert particles == [
        Particle(0, Vector3D(3, 0, 0), Vector3D(2, 0, 0), Vector3D(-1, 0, 0)),
        Particle(1, Vector3D(4, 0, 0), Vector3D(0, 0, 0), Vector3D(-2, 0, 0)),
    ]
