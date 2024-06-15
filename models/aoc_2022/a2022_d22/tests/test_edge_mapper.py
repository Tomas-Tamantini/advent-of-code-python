from models.common.vectors import Vector2D, CardinalDirection
from ..logic import CubeNavigator, CubeNet, PacmanEdgeMapper

net = CubeNet(
    edge_length=10,
    cube_faces_planar_positions={
        "bottom": Vector2D(1, 1),
        "left": Vector2D(0, 1),
        "back": Vector2D(1, 0),
        "right": Vector2D(2, 1),
        "front": Vector2D(1, 2),
        "top": Vector2D(1, 3),
    },
)


def test_pacman_edge_mapper_sends_navigator_travelling_east_to_leftmost_side_of_cube_net():
    cube_navigator = CubeNavigator(
        cube_face="right",
        relative_position=Vector2D(9, 3),
        facing=CardinalDirection.EAST,
    )
    expected_navigator = CubeNavigator(
        cube_face="left",
        relative_position=Vector2D(0, 3),
        facing=CardinalDirection.EAST,
    )
    edge_mapper = PacmanEdgeMapper(net)
    assert expected_navigator == edge_mapper.next_navigator_state(cube_navigator)


def test_pacman_edge_mapper_sends_navigator_travelling_west_to_rightmost_side_of_cube_net():
    cube_navigator = CubeNavigator(
        cube_face="top",
        relative_position=Vector2D(0, 4),
        facing=CardinalDirection.WEST,
    )
    expected_navigator = CubeNavigator(
        cube_face="top",
        relative_position=Vector2D(9, 4),
        facing=CardinalDirection.WEST,
    )
    edge_mapper = PacmanEdgeMapper(net)
    assert expected_navigator == edge_mapper.next_navigator_state(cube_navigator)


def test_pacman_edge_mapper_sends_navigator_travelling_south_to_topmost_side_of_cube_net():
    cube_navigator = CubeNavigator(
        cube_face="right",
        relative_position=Vector2D(9, 9),
        facing=CardinalDirection.SOUTH,
    )
    expected_navigator = CubeNavigator(
        cube_face="right",
        relative_position=Vector2D(9, 0),
        facing=CardinalDirection.SOUTH,
    )
    edge_mapper = PacmanEdgeMapper(net)
    assert expected_navigator == edge_mapper.next_navigator_state(cube_navigator)


def test_pacman_edge_mapper_sends_navigator_travelling_north_to_bottommost_side_of_cube_net():
    cube_navigator = CubeNavigator(
        cube_face="bottom",
        relative_position=Vector2D(3, 0),
        facing=CardinalDirection.NORTH,
    )
    expected_navigator = CubeNavigator(
        cube_face="top",
        relative_position=Vector2D(3, 9),
        facing=CardinalDirection.NORTH,
    )
    edge_mapper = PacmanEdgeMapper(net)
    assert expected_navigator == edge_mapper.next_navigator_state(cube_navigator)
