from typing import Iterator

from models.common.io import InputReader

from .fabric_area import FabricRectangle


def _parse_fabric_rectangle(line: str) -> FabricRectangle:
    parts = line.strip().split(" ")
    rect_id = int(parts[0].replace("#", ""))
    inches_from_left, inches_from_top = map(int, parts[2].replace(":", "").split(","))
    width, height = map(int, parts[3].split("x"))
    return FabricRectangle(rect_id, inches_from_left, inches_from_top, width, height)


def parse_fabric_rectangles(input_reader: InputReader) -> Iterator[FabricRectangle]:
    for line in input_reader.readlines():
        yield _parse_fabric_rectangle(line)
