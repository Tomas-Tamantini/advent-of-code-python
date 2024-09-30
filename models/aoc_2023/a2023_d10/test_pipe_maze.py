from models.common.vectors import Vector2D, CardinalDirection
from models.common.io import CharacterGrid
from .pipe_maze import PipeMaze, PipeSegment


def test_can_enter_pipe_segment_from_one_of_its_two_directions():
    segment = PipeSegment(CardinalDirection.NORTH, CardinalDirection.EAST)
    assert segment.can_enter_from(CardinalDirection.NORTH)
    assert segment.can_enter_from(CardinalDirection.EAST)
    assert not segment.can_enter_from(CardinalDirection.SOUTH)
    assert not segment.can_enter_from(CardinalDirection.WEST)


def test_pipe_segment_exit_direction_depends_on_enter_direction():
    segment = PipeSegment(CardinalDirection.NORTH, CardinalDirection.EAST)
    assert (
        segment.exit_direction(enter_direction=CardinalDirection.SOUTH)
        == CardinalDirection.EAST
    )
    assert (
        segment.exit_direction(enter_direction=CardinalDirection.WEST)
        == CardinalDirection.NORTH
    )


def _build_maze() -> PipeMaze:
    maze_text = """
                7S-7|
                L|7||
                -L-J|
                L|-.F
                """
    grid = CharacterGrid(maze_text)
    return PipeMaze(grid)


def test_pipe_maze_has_starting_point():
    maze = _build_maze()
    start_position = next(maze.loop_positions())
    assert start_position == Vector2D(1, 0)


def test_pipe_moves_through_all_points_in_loop():
    maze = _build_maze()
    positions = tuple(maze.loop_positions())
    assert positions == (
        Vector2D(1, 0),
        Vector2D(2, 0),
        Vector2D(3, 0),
        Vector2D(3, 1),
        Vector2D(3, 2),
        Vector2D(2, 2),
        Vector2D(1, 2),
        Vector2D(1, 1),
    )
