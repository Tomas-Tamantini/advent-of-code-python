from models.common.io import InputReader
from models.common.vectors import BoundingBox, Vector2D


def parse_bounding_box(input_reader: InputReader) -> BoundingBox:
    line = input_reader.read().strip()
    parts = line.split(",")
    x_parts = parts[0].split("=")[-1]
    y_parts = parts[1].split("=")[-1]
    x_min, x_max = map(int, x_parts.split(".."))
    y_min, y_max = map(int, y_parts.split(".."))
    return BoundingBox(
        bottom_left=Vector2D(x_min, y_min), top_right=Vector2D(x_max, y_max)
    )
