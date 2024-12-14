from typing import Iterator

from models.common.io import InputReader
from models.common.vectors import Particle2D, Vector2D


def parse_moving_particles(input_reader: InputReader) -> Iterator[Particle2D]:
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
        yield Particle2D(position, velocity)
