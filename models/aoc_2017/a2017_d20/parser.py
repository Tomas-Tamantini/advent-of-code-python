from typing import Iterator
from models.common.io import InputReader
from models.common.vectors import Vector3D
from .particle_collider import Particle


def parse_particles(input_reader: InputReader) -> Iterator[Particle]:
    for particle_id, line in enumerate(input_reader.readlines()):
        parts = line.strip().split(">,")
        position = Vector3D(*map(int, parts[0].replace("p=<", "").split(",")))
        velocity = Vector3D(*map(int, parts[1].replace("v=<", "").split(",")))
        acceleration = Vector3D(
            *map(int, parts[2].replace("a=<", "").replace(">", "").split(","))
        )
        yield Particle(particle_id, position, velocity, acceleration)
