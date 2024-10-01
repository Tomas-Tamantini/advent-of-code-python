import pytest
from models.common.vectors import Vector2D, CardinalDirection
from ..logic import LightBeam


@pytest.mark.parametrize(
    "direction, next_position",
    [
        (CardinalDirection.EAST, Vector2D(6, 5)),
        (CardinalDirection.WEST, Vector2D(4, 5)),
        (CardinalDirection.NORTH, Vector2D(5, 4)),
        (CardinalDirection.SOUTH, Vector2D(5, 6)),
    ],
)
def test_light_beam_moves_along_its_direction(direction, next_position):
    beam = LightBeam(position=Vector2D(5, 5), direction=direction)
    assert beam.move_forward() == LightBeam(position=next_position, direction=direction)
