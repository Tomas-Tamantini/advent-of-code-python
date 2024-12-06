import pytest

from models.common.io import InputFromString
from models.common.vectors import CardinalDirection, Vector2D

from ..logic import LightBeam
from ..parser import parse_mirror_contraption


@pytest.mark.parametrize(
    ("beam", "next_beams"),
    [
        (
            LightBeam(Vector2D(0, 0), CardinalDirection.EAST),
            {LightBeam(Vector2D(1, 0), CardinalDirection.EAST)},
        ),
        (
            LightBeam(Vector2D(9, 3), CardinalDirection.EAST),
            set(),
        ),
        (
            LightBeam(Vector2D(4, 1), CardinalDirection.SOUTH),
            {LightBeam(Vector2D(5, 1), CardinalDirection.EAST)},
        ),
        (
            LightBeam(Vector2D(0, 1), CardinalDirection.WEST),
            {
                LightBeam(Vector2D(0, 0), CardinalDirection.NORTH),
                LightBeam(Vector2D(0, 2), CardinalDirection.SOUTH),
            },
        ),
    ],
)
def test_parse_initialization_sequence(beam, next_beams):
    file_content = r""".|...\....
                       |.-.\.....
                       .....|-...
                       ........|.
                       ..........
                       .........\
                       ..../.\\..
                       .-.-/..|..
                       .|....-|.\
                       ..//.|...."""
    input_reader = InputFromString(file_content)
    contraption = parse_mirror_contraption(input_reader)
    assert set(contraption.propagate(beam)) == next_beams
