from models.common.io import InputFromString
from ..parser import parse_reindeers


def test_parse_reindeer():
    input_reader = InputFromString(
        "Dancer can fly 27 km/s for 5 seconds, but then must rest for 132 seconds."
    )
    reindeers = parse_reindeers(input_reader)
    reindeer = next(reindeers)
    assert reindeer.flight_speed == 27
    assert reindeer.flight_interval == 5
    assert reindeer.rest_interval == 132
