from typing import Iterator
from models.common.io import InputReader
from models.common.vectors import Vector2D
from .moving_particles import MovingParticle


def parse_moving_particles(input_reader: InputReader) -> Iterator[MovingParticle]:
    for line in input_reader.readlines():
        stripped_line = (
            line.strip()
            .replace(">", "")
            .replace("position=<", "")
            .replace("velocity=<", ",")
        )
        coords = list(map(int, stripped_line.split(",")))
        position = Vector2D(*coords[:2])
        velocity = Vector2D(*coords[2:])
        yield MovingParticle(position, velocity)
