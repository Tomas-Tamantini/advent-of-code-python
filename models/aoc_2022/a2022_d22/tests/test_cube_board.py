from unittest.mock import Mock
from models.common.vectors import Vector2D, CardinalDirection
from ..logic import CubeBoard, BoardNavigator, PacmanEdgeMapper, CubeNet, CubeFace


def test_cube_board_initial_position_is_first_open_position_on_first_row():
    cube_net = Mock()
    cube_net.topmost_left_position.return_value = Vector2D(123, 321)
    edge_mapper = Mock()
    edge_mapper.cube_net = cube_net
    board = CubeBoard(edge_mapper)
    assert board.initial_position == Vector2D(123, 321)


def test_next_navigator_on_board_is_cell_n_steps_away_if_it_is_open():
    face = CubeFace(walls=frozenset())
    cube_net = CubeNet(
        edge_length=50, cube_faces_planar_positions={face: Vector2D(0, 0)}
    )
    edge_mapper = PacmanEdgeMapper(cube_net)
    board = CubeBoard(edge_mapper)
    navigator = BoardNavigator(position=Vector2D(11, 2), facing=CardinalDirection.EAST)
    next_navigator = board.move_navigator_forward(navigator, num_steps=3)
    assert next_navigator.position == Vector2D(14, 2)


def test_next_navigator_on_cube_board_moves_to_new_edge_indicated_by_edge_mapper():
    face = CubeFace(walls=frozenset())
    cube_net = CubeNet(
        edge_length=10, cube_faces_planar_positions={face: Vector2D(0, 0)}
    )
    edge_mapper = PacmanEdgeMapper(cube_net)
    board = CubeBoard(edge_mapper)
    navigator = BoardNavigator(position=Vector2D(5, 2), facing=CardinalDirection.EAST)
    next_navigator = board.move_navigator_forward(navigator, num_steps=6)
    assert next_navigator.position == Vector2D(1, 2)


def test_next_navigator_on_board_stops_just_before_obstacle():
    face = CubeFace(walls=frozenset([Vector2D(10, 0)]))
    cube_net = CubeNet(
        edge_length=100, cube_faces_planar_positions={face: Vector2D(0, 0)}
    )
    edge_mapper = PacmanEdgeMapper(cube_net)
    board = CubeBoard(edge_mapper)
    navigator = BoardNavigator(position=Vector2D(0, 0), facing=CardinalDirection.EAST)
    next_navigator = board.move_navigator_forward(navigator, num_steps=100)
    assert next_navigator.position == Vector2D(9, 0)
