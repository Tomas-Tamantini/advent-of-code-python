from models.common.io import CharacterGrid
from models.common.vectors import Vector2D, CardinalDirection
from ..parser import parse_patrol_area, parse_patrol_guard


_GRID = CharacterGrid(
    """
    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    """
)


def test_parse_patrol_area():
    patrol_area = parse_patrol_area(_GRID)
    assert patrol_area.is_obstacle(Vector2D(2, 3))
    assert not patrol_area.is_obstacle(Vector2D(2, 2))
    assert patrol_area.is_out_of_bounds(Vector2D(1, 9))
    assert not patrol_area.is_out_of_bounds(Vector2D(1, 8))


def test_parse_patrol_guard():
    guard = parse_patrol_guard(_GRID)
    assert guard.position == Vector2D(4, 6)
    assert guard.direction == CardinalDirection.NORTH
