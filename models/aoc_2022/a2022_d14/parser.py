from typing import Iterator
from models.common.io import InputReader
from models.common.vectors import Vector2D


def _line_connecting(start: Vector2D, end: Vector2D) -> Iterator[Vector2D]:
    if start.x == end.x:
        for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
            yield Vector2D(start.x, y)
    elif start.y == end.y:
        for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
            yield Vector2D(x, start.y)


def _parse_chained_obstacles(line: str) -> Iterator[Vector2D]:
    positions_str = line.split(" ->")
    positions = [Vector2D(*map(int, pos.split(","))) for pos in positions_str]
    for pair_index in range(len(positions) - 1):
        yield from _line_connecting(positions[pair_index], positions[pair_index + 1])


def parse_obstacles(input_reader: InputReader) -> Iterator[Vector2D]:
    for line in input_reader.read_stripped_lines():
        yield from _parse_chained_obstacles(line)
