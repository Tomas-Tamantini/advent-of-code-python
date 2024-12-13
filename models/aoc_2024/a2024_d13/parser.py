from typing import Iterator

from models.common.io import InputReader
from models.common.vectors import Vector2D

from .claw_machine import ClawMachine


def _parse_vector(vector_str: str) -> Vector2D:
    coord_values = (
        vector_str.split(":")[1]
        .strip()
        .replace("X", "")
        .replace("Y", "")
        .replace("+", "")
        .replace("=", "")
        .split(",")
    )
    return Vector2D(*map(int, coord_values))


def parse_claw_machines(input_reader: InputReader) -> Iterator[ClawMachine]:
    lines = list(input_reader.read_stripped_lines())
    for i in range(0, len(lines), 3):
        yield ClawMachine(
            btn_a_offset=_parse_vector(lines[i]),
            btn_b_offset=_parse_vector(lines[i + 1]),
            prize_location=_parse_vector(lines[i + 2]),
        )
