from ..logic import WindGenerator
from models.common.vectors import CardinalDirection


def test_wind_generator_loops_around_wind_directions_endlessy():
    directions = [
        CardinalDirection.EAST,
        CardinalDirection.WEST,
        CardinalDirection.WEST,
    ]
    generator = WindGenerator(directions=directions)
    directions = []
    for _ in range(5):
        directions.append(generator.wind_direction())
        generator = generator.increment()

    assert directions == [
        CardinalDirection.EAST,
        CardinalDirection.WEST,
        CardinalDirection.WEST,
        CardinalDirection.EAST,
        CardinalDirection.WEST,
    ]
