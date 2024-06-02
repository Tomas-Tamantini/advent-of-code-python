from typing import Iterator
from models.common.io import InputReader
from models.common.vectors import Vector3D
from .nanobot import TeleportNanobot


def parse_nanobots(input_reader: InputReader) -> Iterator[TeleportNanobot]:
    for line in input_reader.readlines():
        numbers = tuple(
            map(
                int,
                line.replace("pos=<", "").replace(">", "").replace("r=", "").split(","),
            )
        )
        yield TeleportNanobot(radius=numbers[-1], position=Vector3D(*numbers[:3]))
