from models.common.vectors import CardinalDirection, Vector2D

from ..logic import CubeNavigator


def test_next_cube_navigator_is_adjacent_position():
    navigator = CubeNavigator(
        face_planar_position=Vector2D(2, 4), facing=CardinalDirection.NORTH
    )
    assert navigator.next_position() == Vector2D(2, 3)
