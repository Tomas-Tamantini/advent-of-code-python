import pytest
from models.common.vectors import Vector2D, CardinalDirection
from ..logic import CubeNavigator, CubeFace


@pytest.mark.parametrize(
    "relative_position, facing, expected",
    [
        (Vector2D(20, 20), CardinalDirection.EAST, False),
        (Vector2D(0, 0), CardinalDirection.SOUTH, False),
        (Vector2D(0, 13), CardinalDirection.WEST, True),
        (Vector2D(13, 0), CardinalDirection.NORTH, True),
        (Vector2D(49, 13), CardinalDirection.EAST, True),
        (Vector2D(13, 49), CardinalDirection.SOUTH, True),
    ],
)
def test_cube_navigator_checks_whether_about_leave_cube_face(
    relative_position, facing, expected
):
    navigator = CubeNavigator("front", relative_position, facing)
    assert navigator.is_about_to_leave_cube_face(edge_length=50) is expected


def test_cube_navigator_checks_whether_they_hit_wall():
    face = CubeFace(walls=frozenset([Vector2D(10, 0)]))
    navigator = CubeNavigator(
        cube_face=face,
        relative_position=Vector2D(0, 0),
        facing=CardinalDirection.EAST,
    )
    assert not navigator.hit_wall()

    navigator = CubeNavigator(
        cube_face=face,
        relative_position=Vector2D(10, 0),
        facing=CardinalDirection.EAST,
    )
    assert navigator.hit_wall()
