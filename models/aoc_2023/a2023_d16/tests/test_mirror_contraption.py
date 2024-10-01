import pytest
from models.common.vectors import Vector2D, CardinalDirection
from ..logic import LightBeam, MirrorContraption


@pytest.mark.parametrize(
    "beam",
    [
        LightBeam(position=Vector2D(9, 5), direction=CardinalDirection.EAST),
        LightBeam(position=Vector2D(0, 5), direction=CardinalDirection.WEST),
        LightBeam(position=Vector2D(5, 0), direction=CardinalDirection.NORTH),
        LightBeam(position=Vector2D(5, 9), direction=CardinalDirection.SOUTH),
    ],
)
def test_light_beam_leaving_edge_of_contraption_disappears(beam):
    contraption = MirrorContraption(width=10, height=10)
    next_beams = list(contraption.propagate(beam))
    assert len(next_beams) == 0


def test_light_beam_on_empty_cell_inside_contraption_continues_in_same_direction():
    contraption = MirrorContraption(width=10, height=10)
    beam = LightBeam(position=Vector2D(5, 5), direction=CardinalDirection.EAST)
    next_beams = list(contraption.propagate(beam))
    assert len(next_beams) == 1
    assert next_beams[0] == LightBeam(
        position=Vector2D(6, 5), direction=CardinalDirection.EAST
    )


# TODO: Add tests for the two types of mirrors and the two types of splitters.
# Maybe create an interface (ContraptionCell), with 3 implementations: EmptyCell, Mirror, Splitter, and pass
# a dictionary of Vector2D -> ContraptionCell to the MirrorContraption constructor (EmptyCell by default).
# The interface could have this method:
# def next_directions(current_beam_direction: CardinalDirection) -> Iterator[CardinalDirection]
