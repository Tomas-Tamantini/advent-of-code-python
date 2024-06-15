from models.common.vectors import Vector2D, CardinalDirection
from ..logic import CubeNet, CubeNavigator, BoardNavigator

net = CubeNet(
    edge_length=50,
    cube_faces_planar_positions={
        "bottom": Vector2D(1, 1),
        "left": Vector2D(0, 1),
        "back": Vector2D(1, 0),
        "right": Vector2D(2, 1),
        "front": Vector2D(1, 2),
        "top": Vector2D(1, 3),
    },
)


def test_cube_net_can_convert_cube_navigator_to_board_navigator_and_vice_versa():
    cube_navigator = CubeNavigator(
        cube_face="right",
        relative_position=Vector2D(2, 3),
        facing=CardinalDirection.NORTH,
    )
    board_navigator = BoardNavigator(
        position=Vector2D(102, 53), facing=CardinalDirection.NORTH
    )
    assert board_navigator == net.cube_navigator_to_board_navigator(cube_navigator)
    assert cube_navigator == net.board_navigator_to_cube_navigator(board_navigator)


def test_cube_net_returns_faces_on_given_row():
    assert {"left", "bottom", "right"} == set(net.faces_on_row(1))


def test_cube_net_returns_faces_on_given_column():
    assert {"back", "bottom", "front", "top"} == set(net.faces_on_column(1))


def test_cube_net_stores_face_positions():
    assert Vector2D(1, 3) == net.face_position("top")
