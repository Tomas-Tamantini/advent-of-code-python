from models.common.vectors import Vector2D, CardinalDirection
from models.common.number_theory import Interval
from ..logic import ObstacleBoard, BoardNavigator


def test_obstacle_board_initial_position_is_first_open_position_on_first_row():
    rows = (Interval(8, 10), Interval(8, 10), Interval(9, 20))
    board = ObstacleBoard(rows, wall_positions=set())
    assert board.initial_position == Vector2D(8, 0)


def test_next_position_on_board_is_cell_n_steps_away_if_it_is_open():
    rows = (Interval(8, 10), Interval(8, 10), Interval(9, 20))
    board = ObstacleBoard(rows, wall_positions=set())
    navigator = BoardNavigator(position=Vector2D(11, 2), facing=CardinalDirection.EAST)
    next_position = board.next_position(navigator, num_steps=3)
    assert next_position == Vector2D(14, 2)


def test_next_position_on_board_wraps_around_horizontally_if_off_edge():
    rows = (Interval(8, 10), Interval(8, 10), Interval(9, 20))
    board = ObstacleBoard(rows, wall_positions=set())
    navigator = BoardNavigator(position=Vector2D(11, 2), facing=CardinalDirection.EAST)
    next_position = board.next_position(navigator, num_steps=30)
    assert next_position == Vector2D(17, 2)

    navigator = BoardNavigator(position=Vector2D(11, 2), facing=CardinalDirection.WEST)
    next_position = board.next_position(navigator, num_steps=4)
    assert next_position == Vector2D(19, 2)


def test_next_position_on_board_wraps_around_vertically_if_off_edge():
    rows = (Interval(8, 10), Interval(8, 10), Interval(9, 20), Interval(9, 20))
    board = ObstacleBoard(rows, wall_positions=set())
    navigator = BoardNavigator(position=Vector2D(9, 0), facing=CardinalDirection.SOUTH)
    next_position = board.next_position(navigator, num_steps=4)
    assert next_position == Vector2D(9, 0)

    navigator = BoardNavigator(position=Vector2D(9, 0), facing=CardinalDirection.NORTH)
    next_position = board.next_position(navigator, num_steps=5)
    assert next_position == Vector2D(9, 3)


def test_next_position_on_board_is_just_before_obstacle_if_one_is_on_the_way():
    rows = (Interval(0, 100),)
    board = ObstacleBoard(rows, wall_positions={Vector2D(10, 0)})
    navigator = BoardNavigator(position=Vector2D(0, 0), facing=CardinalDirection.EAST)
    next_position = board.next_position(navigator, num_steps=100)
    assert next_position == Vector2D(9, 0)
