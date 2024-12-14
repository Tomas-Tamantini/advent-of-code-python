from typing import Iterator

from models.common.io import InputReader
from models.common.vectors import Particle2D, Vector2D


def _parse_security_robot(line: str) -> Particle2D:
    """p=6,3 v=-1,-3"""
    parts = line.replace("p", "").replace("v", "").replace("=", "").split()
    return Particle2D(
        position=Vector2D(*map(int, parts[0].split(","))),
        velocity=Vector2D(*map(int, parts[1].split(","))),
    )


def parse_security_robots(input_reader: InputReader) -> Iterator[Particle2D]:
    for line in input_reader.read_stripped_lines():
        yield _parse_security_robot(line)
