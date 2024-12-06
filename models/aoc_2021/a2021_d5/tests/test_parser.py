from models.common.io import InputFromString
from models.common.vectors import Vector2D

from ..line_segment import LineSegment
from ..parser import parse_line_segments


def test_parse_line_segments():
    file_content = """0,9 -> 5,9
                      8,0 -> 0,8"""
    segments = list(parse_line_segments(InputFromString(file_content)))
    assert segments == [
        LineSegment(start=Vector2D(0, 9), end=Vector2D(5, 9)),
        LineSegment(start=Vector2D(8, 0), end=Vector2D(0, 8)),
    ]
