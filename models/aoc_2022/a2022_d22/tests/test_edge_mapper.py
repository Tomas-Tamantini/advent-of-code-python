from models.common.vectors import Vector2D, CardinalDirection
from ..logic import CubeNavigator, CubeNet, PacmanEdgeMapper

cube_sides = {
    "bottom": Vector2D(1, 1),
    "left": Vector2D(0, 1),
    "back": Vector2D(1, 0),
    "right": Vector2D(2, 1),
    "front": Vector2D(1, 2),
    "top": Vector2D(1, 3),
}

net = CubeNet(face_planar_positions=set(cube_sides.values()))


def test_pacman_edge_mapper_sends_navigator_to_adjacent_face_if_one_exists():
    cube_navigator = CubeNavigator(
        face_planar_position=cube_sides["left"],
        facing=CardinalDirection.EAST,
    )
    expected_navigator = CubeNavigator(
        face_planar_position=cube_sides["bottom"],
        facing=CardinalDirection.EAST,
    )
    edge_mapper = PacmanEdgeMapper(net)
    assert expected_navigator == edge_mapper.next_navigator(cube_navigator)


def test_pacman_edge_mapper_sends_navigator_travelling_east_to_leftmost_face_on_same_row_if_no_adjacent_face():
    cube_navigator = CubeNavigator(
        face_planar_position=cube_sides["right"],
        facing=CardinalDirection.EAST,
    )
    expected_navigator = CubeNavigator(
        face_planar_position=cube_sides["left"],
        facing=CardinalDirection.EAST,
    )
    edge_mapper = PacmanEdgeMapper(net)
    assert expected_navigator == edge_mapper.next_navigator(cube_navigator)


def test_pacman_edge_mapper_sends_navigator_travelling_west_to_rightmost_face_on_same_row_if_no_adjacent_face():
    cube_navigator = CubeNavigator(
        face_planar_position=cube_sides["top"],
        facing=CardinalDirection.WEST,
    )
    expected_navigator = CubeNavigator(
        face_planar_position=cube_sides["top"],
        facing=CardinalDirection.WEST,
    )
    edge_mapper = PacmanEdgeMapper(net)
    assert expected_navigator == edge_mapper.next_navigator(cube_navigator)


def test_pacman_edge_mapper_sends_navigator_travelling_south_to_topmost_face_on_same_column_if_no_adjacent_face():
    cube_navigator = CubeNavigator(
        face_planar_position=cube_sides["right"],
        facing=CardinalDirection.SOUTH,
    )
    expected_navigator = CubeNavigator(
        face_planar_position=cube_sides["right"],
        facing=CardinalDirection.SOUTH,
    )
    edge_mapper = PacmanEdgeMapper(net)
    assert expected_navigator == edge_mapper.next_navigator(cube_navigator)


def test_pacman_edge_mapper_sends_navigator_travelling_north_to_bottommost_face_on_same_column_if_no_adjacent_face():
    cube_navigator = CubeNavigator(
        face_planar_position=cube_sides["back"],
        facing=CardinalDirection.NORTH,
    )
    expected_navigator = CubeNavigator(
        face_planar_position=cube_sides["top"],
        facing=CardinalDirection.NORTH,
    )
    edge_mapper = PacmanEdgeMapper(net)
    assert expected_navigator == edge_mapper.next_navigator(cube_navigator)
