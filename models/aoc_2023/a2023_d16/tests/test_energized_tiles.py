from models.common.vectors import CardinalDirection, Vector2D

from ..logic import LightBeam, Mirror, MirrorContraption, Splitter, num_energized_tiles

_contraption = MirrorContraption(
    width=10,
    height=10,
    cells={
        Vector2D(x=2, y=9): Mirror(is_upward_diagonal=True),
        Vector2D(x=3, y=9): Mirror(is_upward_diagonal=True),
        Vector2D(x=4, y=7): Mirror(is_upward_diagonal=True),
        Vector2D(x=4, y=6): Mirror(is_upward_diagonal=True),
        Vector2D(x=4, y=1): Mirror(is_upward_diagonal=False),
        Vector2D(x=5, y=0): Mirror(is_upward_diagonal=False),
        Vector2D(x=6, y=6): Mirror(is_upward_diagonal=False),
        Vector2D(x=7, y=6): Mirror(is_upward_diagonal=False),
        Vector2D(x=9, y=5): Mirror(is_upward_diagonal=False),
        Vector2D(x=9, y=8): Mirror(is_upward_diagonal=False),
        Vector2D(x=2, y=1): Splitter(is_horizontal=True),
        Vector2D(x=6, y=2): Splitter(is_horizontal=True),
        Vector2D(x=1, y=7): Splitter(is_horizontal=True),
        Vector2D(x=3, y=7): Splitter(is_horizontal=True),
        Vector2D(x=6, y=8): Splitter(is_horizontal=True),
        Vector2D(x=1, y=0): Splitter(is_horizontal=False),
        Vector2D(x=0, y=1): Splitter(is_horizontal=False),
        Vector2D(x=5, y=2): Splitter(is_horizontal=False),
        Vector2D(x=8, y=3): Splitter(is_horizontal=False),
        Vector2D(x=7, y=7): Splitter(is_horizontal=False),
        Vector2D(x=1, y=8): Splitter(is_horizontal=False),
        Vector2D(x=7, y=8): Splitter(is_horizontal=False),
        Vector2D(x=5, y=9): Splitter(is_horizontal=False),
    },
)


def test_num_energized_tiles_in_contraption_is_calculated_for_initial_beam():
    initial_beam = LightBeam(Vector2D(0, 0), CardinalDirection.EAST)
    assert 46 == num_energized_tiles(initial_beam, _contraption)
