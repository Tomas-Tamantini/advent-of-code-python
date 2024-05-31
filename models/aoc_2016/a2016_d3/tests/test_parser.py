from models.common.io import InputFromString
from ..parser import parse_triangle_sides


def test_parse_triangle_sides():
    file_content = """101 301 501
                      102 302 502
                      103 303 503
                      201 401 601
                      202 402 602
                      203 403 603"""
    input_reader = InputFromString(file_content)
    sides_horizontal = list(parse_triangle_sides(input_reader, read_horizontally=True))
    assert sides_horizontal == [
        (101, 301, 501),
        (102, 302, 502),
        (103, 303, 503),
        (201, 401, 601),
        (202, 402, 602),
        (203, 403, 603),
    ]

    sides_vertical = list(parse_triangle_sides(input_reader, read_horizontally=False))
    assert sides_vertical == [
        (101, 102, 103),
        (301, 302, 303),
        (501, 502, 503),
        (201, 202, 203),
        (401, 402, 403),
        (601, 602, 603),
    ]
