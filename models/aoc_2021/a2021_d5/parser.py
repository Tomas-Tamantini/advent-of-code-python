from typing import Iterator
from models.common.io import InputReader
from models.common.vectors import Vector2D
from .line_segment import LineSegment


def _parse_line_segment(line: str) -> LineSegment:
    parts = line.split("->")
    start = Vector2D(*map(int, parts[0].split(",")))
    end = Vector2D(*map(int, parts[1].split(",")))
    return LineSegment(start, end)


def parse_line_segments(input_reader: InputReader) -> Iterator[LineSegment]:
    for line in input_reader.read_stripped_lines():
        yield _parse_line_segment(line)
