from models.common.vectors import Vector2D, CardinalDirection
from ..logic import CubeNet, CubeNavigator, BoardNavigator


def test_cube_net_can_convert_cube_navigator_to_board_navigator_and_vice_versa():
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
