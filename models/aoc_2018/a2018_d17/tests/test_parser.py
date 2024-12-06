from models.common.io import InputFromString
from models.common.vectors import Vector2D

from ..parser import parse_position_ranges


def test_parse_position_ranges():
    file_content = """x=495, y=2..4
                      y=11..13, x=123
                      x=3, y=4
                      y=1..2, x=1001..1002"""
    positions = set(parse_position_ranges(InputFromString(file_content)))
    assert positions == {
        Vector2D(495, 2),
        Vector2D(495, 3),
        Vector2D(495, 4),
        Vector2D(123, 11),
        Vector2D(123, 12),
        Vector2D(123, 13),
        Vector2D(3, 4),
        Vector2D(1001, 1),
        Vector2D(1001, 2),
        Vector2D(1002, 1),
        Vector2D(1002, 2),
    }
