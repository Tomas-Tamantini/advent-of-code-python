from typing import Iterator

from models.common.io import InputReader
from models.common.vectors import Vector2D


def parse_position_ranges(input_reader: InputReader) -> Iterator[Vector2D]:
    for line in input_reader.readlines():
        parts = line.strip().split(",")
        coords = dict()
        for part in parts:
            key, value = part.split("=")
            min_coord = int(value.split("..")[0])
            max_coord = int(value.split("..")[-1])
            coords[key.strip()] = (min_coord, max_coord)
        for x in range(coords["x"][0], coords["x"][1] + 1):
            for y in range(coords["y"][0], coords["y"][1] + 1):
                yield Vector2D(x, y)
