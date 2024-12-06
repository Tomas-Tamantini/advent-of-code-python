from models.common.io import InputFromString
from models.common.vectors import CardinalDirection

from ..parser import parse_wind_directions


def test_parse_wind_directions():
    input_reader = InputFromString(">><")
    result = list(parse_wind_directions(input_reader))
    assert result == [
        CardinalDirection.EAST,
        CardinalDirection.EAST,
        CardinalDirection.WEST,
    ]
