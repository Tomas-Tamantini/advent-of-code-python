import pytest
from models.common.vectors import Vector2D, CardinalDirection
from ..logic import LightBeam, MirrorContraption, Mirror, Splitter

_contraption = MirrorContraption(
    width=10,
    height=10,
    cells={
        Vector2D(5, 3): Mirror(is_upward_diagonal=True),
        Vector2D(7, 8): Splitter(is_horizontal=False),
    },
)


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
    next_beams = list(_contraption.propagate(beam))
    assert len(next_beams) == 0


def test_default_contraption_cell_is_empty_cell():
    beam = LightBeam(position=Vector2D(5, 5), direction=CardinalDirection.SOUTH)
    next_beams = list(_contraption.propagate(beam))
    assert len(next_beams) == 1
    assert next_beams[0] == LightBeam(
        position=Vector2D(5, 6), direction=CardinalDirection.SOUTH
    )


def test_light_beam_in_contraption_is_reflected_by_mirror():
    beam = LightBeam(position=Vector2D(5, 3), direction=CardinalDirection.EAST)
    next_beams = list(_contraption.propagate(beam))
    assert len(next_beams) == 1
    assert next_beams[0] == LightBeam(
        position=Vector2D(5, 2), direction=CardinalDirection.NORTH
    )


def test_light_beam_in_contraption_is_split_by_splitter():
    beam = LightBeam(position=Vector2D(7, 8), direction=CardinalDirection.WEST)
    next_beams = list(_contraption.propagate(beam))
    assert len(next_beams) == 2
    assert set(next_beams) == {
        LightBeam(position=Vector2D(7, 7), direction=CardinalDirection.NORTH),
        LightBeam(position=Vector2D(7, 9), direction=CardinalDirection.SOUTH),
    }
