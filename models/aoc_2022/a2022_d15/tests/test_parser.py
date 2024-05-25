from models.common.io import InputFromString
from models.common.vectors import Vector2D
from ..parser import parse_proximity_sensors
from ..logic import ProximitySensor


def test_parse_proximity_sensors():
    input_reader = InputFromString(
        """
        Sensor at x=2, y=18: closest beacon is at x=-2, y=15
        Sensor at x=9, y=16: closest beacon is at x=10, y=16
        """
    )
    positions = list(parse_proximity_sensors(input_reader))
    assert positions == [
        ProximitySensor(position=Vector2D(2, 18), nearest_beacon=Vector2D(-2, 15)),
        ProximitySensor(position=Vector2D(9, 16), nearest_beacon=Vector2D(10, 16)),
    ]
