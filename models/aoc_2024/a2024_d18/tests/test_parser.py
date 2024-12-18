from models.common.io import InputFromString
from models.common.vectors import Vector2D

from ..parser import parse_byte_positions


def test_parse_byte_positions():
    file_content = """5,4
                      4,2
                      4,5"""
    input_reader = InputFromString(file_content)
    positions = list(parse_byte_positions(input_reader))
    assert positions == [Vector2D(5, 4), Vector2D(4, 2), Vector2D(4, 5)]
