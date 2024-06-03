from models.common.io import InputFromString
from models.common.vectors import HexagonalDirection
from ..parser import parse_rotated_hexagonal_directions


def test_parse_rotated_hexagonal_directions_without_delimeters():
    file_content = """
                   esenee
                   nwwswee
                   """
    directions = list(parse_rotated_hexagonal_directions(InputFromString(file_content)))
    assert directions == [
        [
            HexagonalDirection.NORTHEAST,
            HexagonalDirection.SOUTHEAST,
            HexagonalDirection.NORTH,
            HexagonalDirection.NORTHEAST,
        ],
        [
            HexagonalDirection.NORTHWEST,
            HexagonalDirection.SOUTHWEST,
            HexagonalDirection.SOUTH,
            HexagonalDirection.NORTHEAST,
            HexagonalDirection.NORTHEAST,
        ],
    ]
