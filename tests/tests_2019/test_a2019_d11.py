from models.common.vectors import Vector2D, CardinalDirection, TurnDirection
from models.aoc_2019.a2019_d11 import (
    Hull,
    HullRobot,
    HullRobotIO,
    run_hull_painting_program,
)


def _build_robot(
    position: Vector2D = Vector2D(0, 0),
    direction: CardinalDirection = CardinalDirection.NORTH,
) -> HullRobot:
    return HullRobot(position=position, direction=direction)


def _build_robot_io(hull: Hull = None, robot: HullRobot = None) -> HullRobotIO:
    if hull is None:
        hull = Hull()
    if robot is None:
        robot = _build_robot()
    return HullRobotIO(hull, robot)


def test_hull_starts_with_all_black_panels():
    hull = Hull()
    assert hull.white_panels == set()


def test_hull_panel_can_be_painted():
    hull = Hull()
    panel = Vector2D(123, 321)
    hull.paint_panel(panel, paint_white=True)
    assert hull.white_panels == {panel}


def test_hull_keeps_track_of_panels_painted_at_least_once():
    hull = Hull()
    hull.paint_panel(Vector2D(0, 0), paint_white=True)
    hull.paint_panel(Vector2D(0, 0), paint_white=False)
    hull.paint_panel(Vector2D(20, 20), paint_white=False)
    assert hull.white_panels == set()
    assert hull.num_panels_painted_at_least_once == 2


def test_can_query_hull_panel_color():
    hull = Hull()
    hull.paint_panel(Vector2D(0, 0), paint_white=True)
    assert hull.is_white(Vector2D(0, 0))
    assert not hull.is_white(Vector2D(0, 1))


def test_hull_robot_can_paint_panel_it_is_currently_on():
    hull = Hull()
    robot = HullRobot(position=Vector2D(0, 0), direction=CardinalDirection.NORTH)
    robot.paint_panel(hull, paint_white=True)
    assert hull.white_panels == {Vector2D(0, 0)}


def test_robot_can_turn_and_move():
    robot = HullRobot(position=Vector2D(0, 0), direction=CardinalDirection.NORTH)
    robot.turn_and_move(TurnDirection.RIGHT)
    assert robot.position == Vector2D(1, 0)
    assert robot.direction == CardinalDirection.EAST


def test_hull_robot_io_yields_0_if_current_panel_is_black():
    robot = _build_robot()
    hull = Hull()
    io = HullRobotIO(hull, robot)
    assert io.read() == 0


def test_hull_robot_io_yields_1_if_current_panel_is_white():
    robot = _build_robot()
    hull = Hull()
    robot.paint_panel(hull, paint_white=True)
    io = HullRobotIO(hull, robot)
    assert io.read() == 1


def test_hull_robot_io_first_output_0_means_paint_panel_black():
    hull = Hull()
    io = _build_robot_io(hull=hull)
    io.write(0)
    assert not hull.is_white(Vector2D(0, 0))


def test_hull_robot_io_first_output_1_means_paint_panel_white():
    hull = Hull()
    io = _build_robot_io(hull=hull)
    io.write(1)
    assert hull.is_white(Vector2D(0, 0))


def test_hull_robot_io_second_ouput_0_means_turn_left():
    robot = _build_robot()
    io = _build_robot_io(robot=robot)
    io.write(1)
    io.write(0)
    assert robot.direction == CardinalDirection.WEST
    assert robot.position == Vector2D(-1, 0)


def test_hull_robot_io_second_ouput_1_means_turn_right():
    robot = _build_robot()
    io = _build_robot_io(robot=robot)
    io.write(1)
    io.write(1)
    assert robot.direction == CardinalDirection.EAST
    assert robot.position == Vector2D(1, 0)


def test_can_count_panels_painted_for_given_program():
    hull = Hull()
    instructions = [104, 1, 104, 0, 104, 0, 104, 1, 99]
    run_hull_painting_program(instructions, hull)
    assert hull.num_panels_painted_at_least_once == 2


def test_can_render_hull_message():
    hull = Hull()
    hull.paint_panel(Vector2D(100, 200), paint_white=True)
    hull.paint_panel(Vector2D(101, 200), paint_white=True)
    hull.paint_panel(Vector2D(102, 201), paint_white=True)
    assert hull.render() == "  #\n## \n"
