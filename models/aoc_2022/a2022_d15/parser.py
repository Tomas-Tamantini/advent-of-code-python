from typing import Iterator

from models.common.io import InputReader
from models.common.vectors import Vector2D

from .logic import ProximitySensor


def _parse_proximity_sensor(line: str) -> ProximitySensor:
    cleaned = line.replace("x=", "").replace("y=", "")
    parts = cleaned.split(":")
    positions = [Vector2D(*map(int, part.split("at")[-1].split(","))) for part in parts]
    return ProximitySensor(position=positions[0], nearest_beacon=positions[1])


def parse_proximity_sensors(input_reader: InputReader) -> Iterator[ProximitySensor]:
    for line in input_reader.read_stripped_lines():
        yield _parse_proximity_sensor(line)
